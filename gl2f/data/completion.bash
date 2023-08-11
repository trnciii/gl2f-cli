__gl2f_complete_boards(){
  if [[ "$cur" == */* ]]; then
    local realcur=${cur##*/}
    local prefix=${cur%/*}
    case ${prefix} in
      ## REPLACE_PAGES_SECOND
    esac
  else
    ## REPLACE_PAGES_FIRST

    if declare -F _init_completion >/dev/null 2>&1; then
      [[ $COMPREPLY == */ ]] && compopt -o nospace # not work on mac
    fi

  fi
}


_gl2f(){
  local cur prev words cword split
  if declare -F _init_completion >/dev/null 2>&1; then
    _init_completion -n :/ || return
  else
    COMPREPLY=()
    _get_comp_words_by_ref -n :/ cur prev words cword || return
  fi

  case $cword in
    1)
      COMPREPLY=( $(compgen -W 'auth cat dl local ls open search completion config' -- "$cur") )
      ;;
    *)
      case ${words[1]} in
        auth)
          COMPREPLY=( $(compgen -W 'file load login remove update set-token' -- "$cur") )
          ;;
        local)
          COMPREPLY=( $(compgen -W 'clear-cache dir index install ls stat open build' -- "$cur") )
          ;;
        config)
          COMPREPLY=( $(compgen -W 'create path view ' -- "$cur") )
          ;;
        cat | dl | ls | open | search)
          __gl2f_complete_boards
          ;;
        esac
      ;;
  esac
}

complete -F _gl2f gl2f
