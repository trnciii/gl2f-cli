_gl2f_init_completion()
{
    COMPREPLY=()
    _get_comp_words_by_ref "$@" cur prev words cword
}


_gl2f(){
	local boards='today blogs/ radio/ news/ gtube cm others shangrila brandnewworld/ daijoubu/ cl fm/ enjoythegooddays famitok/ lovely2live garugakulive chuwapane onlinelive2020'
	local groups='girls2 lucky2 lovely2'
	local mem_G2='yuzuha momoka misaki youka kurea minami kira toa ran'
	local mem_L2='rina yura tsubaki hiro yuwa kanna ririka akari kiki'
	local mem_l2='miyu yui rina yura lovely2staff'

	local cur prev words cword split
	if declare -F _init_completion >/dev/null 2>&1; then
		_init_completion -n :/ || return
	else
		_gl2f_init_completion -n :/ || return
	fi

	case $cword in
		1)
			COMPREPLY=( $(compgen -W 'auth cat dl local ls open search completion' -- "$cur") )
			;;
		*)
			case ${words[1]} in
				auth)
					COMPREPLY=( $(compgen -W 'file load login remove update set-token' -- "$cur") )
					;;
				local)
					COMPREPLY=( $(compgen -W 'clear-cache dir index install ls stat open' -- "$cur") )
					;;
				cat | dl | ls | open | search)
					if [[ "$cur" == */* ]]; then
						local realcur=${cur##*/}
						local prefix=${cur%/*}
						case ${prefix} in
							blogs)
								COMPREPLY=( $(compgen -W "${groups} ${mem_G2} ${mem_L2} ${mem_l2} today" -P "${prefix}/" -- ${realcur}) )
								;;
							radio)
								COMPREPLY=( $(compgen -W "girls2 lucky2 ${mem_G2} ${mem_L2}" -P "${prefix}/" -- ${realcur}) )
								;;
							news)
								COMPREPLY=( $(compgen -W "today family girls2 lovely2 lucky2 mirage2" -P "${prefix}/" -- ${realcur}) )
								;;
							brandnewworld)
								COMPREPLY=( $(compgen -W "photo cheer" -P "${prefix}/" -- ${realcur}) )
								;;
							daijoubu)
								COMPREPLY=( $(compgen -W "photo cheer" -P "${prefix}/" -- ${realcur}) )
								;;
							fm)
								COMPREPLY=( $(compgen -W "girls2 lucky2" -P "${prefix}/" -- ${realcur}) )
								;;
							famitok)
								COMPREPLY=( $(compgen -W "girls2 lucky2" -P "${prefix}/" -- ${realcur}) )
								;;
						esac
					else
						COMPREPLY=( $(compgen -W "${boards}" -- ${cur}) )

						if declare -F _init_completion >/dev/null 2>&1; then
							[[ $COMPREPLY == */ ]] && compopt -o nospace # not work on mac
						fi

					fi
					;;
				esac
			;;
	esac
}

complete -F _gl2f gl2f
