_script()
{ 
  local cur
  COMPREPLY=()
  cur="${COMP_WORDS[COMP_CWORD]}"
  HLS_AUTOCOMPLETE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
  COMMAND=$(python $HLS_AUTOCOMPLETE_DIR/hls_autocomplete/complete.py $cur)
  _script_commands=$COMMAND
  COMPREPLY=( ${_script_commands} )
  return 0
}
complete -o nospace -F _script hls
complete -o nospace -F _script hcat
complete -o nospace -F _script hrm
complete -o nospace -F _script hdu
complete -o nospace -F _script simprot
complete -o nospace -F _script richprot
