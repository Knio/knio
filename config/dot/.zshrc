# disable global rwx
umask 027

# not sure who is supposed to actually set this
export LANG=C.UTF-8
export LESSUTFBINFMT=*n%C

export VISUAL=nano
export EDITOR=nano
export PAGER=less

setopt PROMPT_SUBST
PS1='%K{238}%F{118}%n%F{black}@%F{45}%m %F{209}%~%F{231}%# '
RPS1='ret: %?'

#  %(?..(%?%)) exit code

# `od` to debug keycodes
bindkey  "^[[H"   beginning-of-line
bindkey  "^[[F"   end-of-line
bindkey  "^[[1~"  beginning-of-line
bindkey  "^[[4~"  end-of-line
bindkey  "^[[3~"  delete-char

# `stty -a` to debug control chars
# https://jvns.ca/blog/2024/10/31/ascii-control-characters/


setopt NO_BANG_HIST
setopt SHARE_HISTORY
setopt INC_APPEND_HISTORY
setopt HIST_IGNORE_ALL_DUPS
setopt HIST_REDUCE_BLANKS
setopt HIST_IGNORE_SPACE

HISTSIZE=10000
SAVEHIST=10000
mkdir -p ~/.config/zsh
HISTFILE=~/.config/zsh/history

autoload -U compinit
compinit

[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

function set_term_title() {
  # TODO make work with unicode
  # set term title (screen passes this thru)
  print -Pn "\e]0;$1\a"
}

function set_screen_title() {
  # TODO make work with unicode
  if [[ "$IN_SCREEN" == "1" ]] then
    print -Pn "\033k$1\033\\"
  fi
}

# runs before command
function preexec() {
  print -Pn '%k%f'
  set_term_title "%m: »$1"
  set_screen_title "*$1"

  # TODO: start timer
}


# runs after command finishes (before printing PS*)
function precmd() {
  set_term_title "%m: %~"
  set_screen_title "%~"
}

source ~/knio/config/bash/aliases
