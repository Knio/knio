import atexit
import signal
import sys
import threading
import pickle
import time
import queue
import pathlib
import subprocess
import os

from . import perfetto

_cwd = str(pathlib.Path('.').resolve()) + '/'

_global_tracer = None
def start(*a, **kw):
  global _global_tracer
  _global_tracer = TraceWriter(*a, **kw)
  # atexit only fires after all threads are stopped, so this is a catch-22
  atexit.register(_global_tracer.finish)
  _global_tracer.start()

def finish():
  if _global_tracer:
    _global_tracer.finish()


class TraceWriter:
  def __init__(self, fn=None):
    if not fn:
      nf = time.strftime(f'%Y%m%d-%H%M%S.{time.perf_counter_ns()}')
      self.fn = pathlib.Path(f'_rebugger_trace_{nf}')
    self.file = self.fn.with_suffix('.tracep').open('wb')
    self.tracers = []
    self.start_writer()
    return
    # TODO: func should be a lambda that makes a new ThreadTracer
    # and returns its trace_cb
    # threading.settrace(func)

  def start(self):
    tt = ThreadTracer()
    self.tracers.append(tt)
    tt.start()
    try:
      self.start_strace()
    except Exception as e:
      print(f'Failed to start strace: {e}', file=sys.stdout)

  def stop(self):
    for tt in self.tracers:
      tt.stop()
    self.poll()
    self.tracers[:] = []

  def finish(self):
    if self.stopper.is_set():
      return
    self.stopper.set()
    print('rebugger stopping', file=sys.stderr)
    if self.strace:
      self.strace.send_signal(signal.SIGINT)
      self.strace.wait()
    self.strace_file.close()
    self.writer.join()
    self.stop()
    print('rebugger processing trace logs, please wait and do not kill the process', file=sys.stderr)
    self.file.close()
    perfetto.perfetto_file_from_tracep(self.fn)
    self.fn.with_suffix('.tracep').unlink()
    self.fn.with_suffix('.strace').unlink()

  def __enter__(self):
    self.start()

  def __exit__(self, exc_type, exc_value, traceback):
    self.stop()

  def __del__(self):
    self.finish()

  def poll(self):
    for t in self.tracers:
      while 1:
        try:
          el = t.q.get_nowait()
        except queue.Empty:
          break
        pickle.dump(el, self.file)
    self.file.flush()

  def start_writer(self):
    self.stopper = threading.Event()
    def loop():
      while not self.stopper.wait(0.100):
        self.poll()
    self.writer = threading.Thread(target=loop)
    self.writer.daemon = True
    self.writer.start()

  def start_strace(self):
    self.strace_file = self.fn.with_suffix('.strace').open('wb')
    self.strace = None
    self.strace = subprocess.Popen([
        'sudo', '-n',
        'strace',
        '-p', f'{os.getpid()}',
        '--timestamps=unix,ns',
        '--syscall-times=ns',
      ],
      stdin=subprocess.DEVNULL,
      stderr=self.strace_file,
    )
    time.sleep(0.1)


_logger_qns = {
  'Logger.debug',
  'Logger.info',
  'Logger.warning',
  'Logger.error',
  'Logger.exception',
  'Logger._log',
}

class ThreadTracer:
  def __init__(self, stopper=None):
    self.q = queue.Queue()
    self.tid = threading.get_native_id()
    self.stopper = stopper or threading.Event()
    self.disable_until_frame = None

  def start(self):
    # TODO use sys.setprofile to capture c_call
    # TODO some deadlock here, does setprofile affect all threads?
    current = sys.gettrace()
    # current = sys.getprofile()
    if current:
      raise RuntimeError('There is already a tracer set', current)
    sys.settrace(self.trace_cb)
    # sys.setprofile(self.trace_cb)

  def stop(self):
    self.stopper.set()

  def trace_cb(self, frame, event, arg):
    if self.stopper.is_set():
      sys.settrace(None)
      return None
    ts = time.perf_counter_ns()
    el = ts, self.tid, event,
    rt = self.trace_cb
    if event == 'line':
      no = frame.f_lineno
      qn = frame.f_code.co_qualname
      fn = frame.f_code.co_filename
      if fn.startswith(_cwd):
        fn = fn[len(_cwd):]
      el += fn, qn, no

    elif event == 'call':
      no = frame.f_lineno
      qn = frame.f_code.co_qualname
      fn = frame.f_code.co_filename
      lc = {}
      for k, v in frame.f_locals.items():
        try:
          lc[k] = repr(v)
        except:
          lc[k] = '<REPR ERROR>'
      # special handling to remove spam from logger
      if qn in _logger_qns and frame.f_code.co_filename.endswith('__init__.py'):
        if self.disable_until_frame:
          # already disabled
          return rt
        el = el[0], el[1], 'log', qn, lc
        self.q.put(el)
        self.disable_until_frame = frame
        return rt
      # normal call
      el += qn, lc, fn, no

    elif event == 'return':
      try:
        el += repr(arg),
      except:
        el += '<REPR ERROR>',
      if frame is self.disable_until_frame:
        self.disable_until_frame = None
        el = None

    elif event == 'exception':
      el += repr(arg[1]),

    else:
      print(el)
      print(frame)
      print(arg)

    if el and not self.disable_until_frame:
      self.q.put(el)
    return rt
