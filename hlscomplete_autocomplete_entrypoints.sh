_script()
{ 
  local cur
  COMPREPLY=()
  cur="${COMP_WORDS[COMP_CWORD]}"
  _script_commands=$(_hls_get_completions $cur)
  COMPREPLY=( $(compgen -W "${_script_commands}" -- ${cur}) )
  return 0
}
complete -o nospace -F _script hls
complete -o nospace -F _script hcat
complete -o nospace -F _script hrm
complete -o nospace -F _script hdu
complete -o nospace -F _script simprot
complete -o nospace -F _script richprot
