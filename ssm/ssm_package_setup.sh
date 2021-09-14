main(){
      load_spooki_runtime_dependencies
      # compile_fortran_module
}

compile_fortran_module(){
   this_dir=`pwd`
   message "compiling fortran module"
   if ((${#BASH_SOURCE[@]})); then
   #bash
   shell_source=${BASH_SOURCE[0]}
   elif ((${#KSH_VERSION[@]})); then
   #ksh
   shell_source=${.sh.file}
   fi

   sourced_file="$(cd "$(dirname "${shell_source}")"; pwd -P)/$(basename "${shell_source}")"
   sourced_file_dir=$(dirname $sourced_file)
   cd $sourced_file_dir
   cd ../../lib/python/ci_fstcomp/
   make
   cd $this_dir
}
message(){
   echo $(tput -T xterm setaf 3)$@$(tput -T xterm sgr 0) >&2
   true
}

print_and_do(){
   message $@
   eval $@
}

load_spooki_runtime_dependencies(){
    message "Loading cifstcomp runtime dependencies ..."
    print_and_do . r.load.dot eccc/mrd/rpn/MIG/ENV/migdep/5.1.1
    print_and_do . r.load.dot eccc/mrd/rpn/MIG/ENV/rpnpy/2.1.2
    message "if you dont have pandas >= 1.0.0, use the following package"
    message ". ssmuse-sh -d /fs/ssm/eccc/cmd/cmds/python_packages/python3.6/all/2021.07"
    message "... done loading cifstcomp runtime dependencies."
}

main
