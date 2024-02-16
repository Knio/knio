'''
OpenAI scripts


'''
import argparse
import pathlib

import toml

from openai import OpenAI


config = toml.load("config.toml")['openai']

openai_client = OpenAI(api_key=config['api_key'])


def code_api(args):
  src = pathlib.Path(args.query[0])
  response = response = openai_client.ChatCompletion.create(
    model=args.model,
    temperature=0.2,
    messages=[
        {"role": "system", "content":
          'You are a software engineer specializing in Python and technical writing. '
          'Given the contents of a Python file below, '
          'study the behavior of the code and document the classes, methods, functions, and variables it contains. '
          'Use your knowledge to add and improve docmentation to the code. '
          'Include a docstring for the entire file, summarizing the purpose of the code and the public APIs. '
          'Include docstrings for all classes, methods, and functions. '
          'Make sure your documentation is precise, but also concise. Do not include redundant information such as describing function parameters using just their name if not providing any additional details. '
          'Write your response as valid Python code, identical to the input, with only the docstrings changed. '
          'Use a writing style for your documentation that is easy to read and understand. '
          'Format the output with a maximum line length of 79 characters. '
          'The Python code is below:\n'
        },
        {"role": "user", "content": src.read_text()},
    ]
  )
  print(response)

  new_code = response['choices'][0]['message']['content']
  src.with_suffix(src.suffix + '.ai').write_text(new_code)
  print(new_code)


def main(args):
  if args.chat:
    response = response = openai_client.ChatCompletion.create(
      model=args.model,
      messages=[
        {"role": "system", "content":
            'You are a helpful assistant.\n'
            'Supply simple, clear, concise, and correct answers to questions.\n'
            'Provide references to any facts used.\n'
        },
        {"role": "user", "content": ' '.join(args.query)},
      ]
    )
    print(response)
    return

  if args.image:
    response = openai_client.images.generate(
      model='dall-e-3',
      quality='standard',
      prompt=' '.join(args.query),
      n=1,
      size="1024x1024"
      # size="256x256",
    )
    print(response)
    return

  if args.code:
    code_api(args)
    return


if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)
  parser.add_argument('--chat', action='store_true')
  parser.add_argument('--image', action='store_true')
  parser.add_argument('--code', action='store_true')
  parser.add_argument('--model', type=str, default='gpt-4-1106-preview')
  parser.add_argument('query', type=str, nargs='+')


  args = parser.parse_args()
  main(args)

