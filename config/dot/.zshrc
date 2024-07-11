



set VISUAL=nano
set EDITOR=nano

setopt PROMPT_SUBST
PS1='%F{green}%n%f@%F{blue}%m %F{yellow}%~%f%# '
RPS1='ret: %?'

#  %(?..(%?%)) exit code

# `od` to debug keycodes
bindkey  "^[[H"   beginning-of-line
bindkey  "^[[F"   end-of-line
bindkey  "^[[3~"  delete-char


setopt NO_BANG_HIST
setopt SHARE_HISTORY
setopt INC_APPEND_HISTORY
setopt HIST_IGNORE_ALL_DUPS
setopt HIST_REDUCE_BLANKS
setopt HIST_IGNORE_SPACE


HISTSIZE=10000
SAVEHIST=10000
HISTFILE=~/.history


source ~/knio/config/bash/aliases

[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

