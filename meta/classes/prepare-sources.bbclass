# This task is created specifically as a hook for recipes. Classes shouldn't
# define this task, but should either create their own tasks, or
# _append/_prepend to it, so the recipe author is free to define it directly.
#
# The intent behind this task is to prepare the source tree for building,
# after the fetching and extraction process but before configuration and
# compilation.
#
# This is a common pattern. Often recipes will do one of these today:
# - prepend do_configure, which isn't ideal, as do_configure runs in ${B} now
# - add a postfunc to unpack/patch
# - add their own task between patch and configure
#
# I think it's appropriate for classes to add their own tasks, but recipes
# should be provided more explicit hooks to use for the common cases.

do_prepare_sources () {
}
do_prepare_sources[dirs] = "${S}"
do_prepare_sources[noexec] = "1"
addtask prepare_sources after do_patch before do_configure

python () {
    if d.getVar('do_prepare_sources', False).rstrip():
        d.delVarFlag('do_prepare_sources', 'noexec')
        if 'SRCTREECOVEREDTASKS' in d:
            d.appendVar('SRCTREECOVEREDTASKS', ' do_prepare_sources')
}
