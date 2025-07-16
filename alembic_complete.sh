#!/bin/bash

# Adapted from Cargo's bash completion by the Rust language
# https://github.com/rust-lang/cargo/blob/master/src/etc/cargo.bashcomp.sh
# This code is under MIT License. See end of the file for the full text

_alembic() {
	local cur prev words cword
	_get_comp_words_by_ref cur prev words cword

	# Find the command and the command index
	local cmd_i cmd
	for (( cmd_i=1; cmd_i<$cword; cmd_i++ ))
	do
		if [[ ! "${words[$cmd_i]}" =~ ^- ]]; then
			cmd="${words[$cmd_i]}"
			break
		fi
	done

	local commands='branches current downgrade edit heads history init list_templates merge revision show stamp upgrade'
	local option_nocmd='$commands -h --help --version -c --config -n --name -x --raiseerr'
	local file_options='-c --config, --version-path'
	local any_options='-n --name -x --tag -t --template -m --message --branch-label --rev-id'
	local rev_options='-r --rev-range --depends-on'
	local file_commands='init'
	local rev_commands='downgrade edit merge show stamp upgrade'

	local opt_branches='-h --help -v --verbose'
	local opt_current='-h --help -v --verbose'
	local opt_downgrade='-h --help --sql --tag' # rev
	local opt_edit='-h --help' # rev
	local opt_heads='-h --help -v --verbose --resolve-dependencies'
	local opt_history='-h --help -r --rev-range -v --verbose -i --indicate-current'
	local opt_init='-h --help -t --template --package' # dir
	local opt_list_templates='-h --help'
	local opt_merge='-h --help -m --message --branch-label --rev-id' # revisions|heads
	local opt_revision='-h --help -m --message --autogenerate --sql --head --splice --branch-label --version-path --rev-id --depends-on'
	local opt_show='-h --help' # rev
	local opt_stamp='-h --help --sql --tag --purge' # revisions|heads
	local opt_upgrade='-h --help --sql --tag' # rev

	COMPREPLY=()

	if [[ " ${file_options} " =~ " ${prev} " ]]; then
		_filedir
	elif [[ " ${rev_options} " =~ " ${prev} " && ! "$cur" =~ ^[-+] ]]; then
		local revisions="$(_revisions) head heads current base"
		COMPREPLY=( $( compgen -W "${revisions}" -- "$cur" ) )
	elif [[ " ${any_options} " =~ " ${prev} " ]]; then
		COMPREPLY=()
	elif [[ $cword -le $cmd_i ]]; then
		# Completion before or at the command.
		COMPREPLY=( $( compgen -W "$option_nocmd" -- "$cur" ) )
	else
		local option_var="opt_${cmd}"
		local options="${!option_var}"
		if [[ -z $options ]]; then
			# Fallback to filename completion.
			_filedir
		else
			if [[ " ${rev_commands} " =~ " ${cmd} " && ! "$cur" =~ ^[-+] ]]; then
				options="$options $(_revisions) head heads current base"
			fi
			COMPREPLY=( $( compgen -W "$options" -- "$cur" ) )
		fi
	fi

	return 0
}

_revisions() {
	alembic history | grep -E '^([0-9a-f]{12}|<base>(, )?)+ -> [0-9a-f]{12}' | sed -E 's/^[0-9a-f, <s>]* -> ([0-9a-f]{12}).*$/\1/' | sed 's/\n/ /'
}

complete -F _alembic alembic
complete -F _alembic ale


# LICENSE
#
# Permission is hereby granted, free of charge, to any
# person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the
# Software without restriction, including without
# limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software
# is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice
# shall be included in all copies or substantial portions
# of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF
# ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
# IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
