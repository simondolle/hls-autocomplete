_script()
{ 
  local cur
  COMPREPLY=()
  cur="${COMP_WORDS[COMP_CWORD]}"
  COMMAND=$(_hls_get_completions $cur)
  _script_commands=$COMMAND
  if [[ $_script_commands == "" ]]; then
    hls $cur &> /dev/null
    _script_commands=$COMMAND
  fi
  COMPREPLY=( ${_script_commands} )
  return 0
}
complete -o nospace -F _script hls
complete -o nospace -F _script hcat
complete -o nospace -F _script hrm
complete -o nospace -F _script hdu
complete -o nospace -F _script simprot
complete -o nospace -F _script richprot
