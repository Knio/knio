
set VISUAL=nano
set EDITOR=nano

setopt PROMPT_SUBST
PS1='%F{green}%n%f@%F{blue}%m %F{yellow}%~%f%# '
RPS1='ret: %?'

#  %(?..(%?%)) exit code

# `od` to debug keycodes
bindkey  "^[[H"   beginning-of-line
bindkey  "^[[F"   end-of-line
bindkey  "^[[1~"  beginning-of-line
bindkey  "^[[4~"  end-of-line
bindkey  "^[[3~"  delete-char

setopt NO_BANG_HIST
setopt SHARE_HISTORY
setopt INC_APPEND_HISTORY
setopt HIST_IGNORE_ALL_DUPS
setopt HIST_REDUCE_BLANKS
setopt HIST_IGNORE_SPACE

HISTSIZE=10000
SAVEHIST=10000
HISTFILE=~/.zsh_history

source ~/knio/config/bash/aliases

autoload -U compinit
compinit

[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh


# runs before command
function preexec() {
  # set term title (screen passes this thru)
  print -Pn "\e]0;%m: ~█~ $1\a"

  # set screen title
  if [[ "$IN_SCREEN" == "1" ]] then
    print -Pn "\033k ~█~ $1\033\\"
  fi
}


# runs after command finishes (before printing PS*)
function precmd() {
  # set term title (screen passes this thru)
  print -Pn "\e]0;%m: %~\a"

  # set screen title
  if [[ "$IN_SCREEN" == "1" ]] then
    print -Pn "\033k%~\033\\"
  fi
}
