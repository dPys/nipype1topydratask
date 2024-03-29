#!/usr/env python
# @dPys and @anibalsolon
# 9/13/2019

'''
A tool for converting nipype interfaces to nipype 2.0 (i.e. pydra) tasks
'''

# Nipype1topydratask
def Nipype1topydratask(interface):
    import pydra
    from pydra.engine.task import ShellCommandTask
    from nipype.utils.functions import create_function_from_source
    from nipype.interfaces import utility as niu
    from nipype.interfaces import base as bs
    from nipype.pipeline import engine as pe

    if not isinstance(interface, pe.Node):
        # Set the Node name
        if isinstance(interface, bs.CommandLine):
            node_name = interface.cmd
        elif isinstance(interface, niu.Function):
            node_name = interface.fullname
        else:
            node_name = interface.__class__.__name__

        # Make a Node
        interface = pe.Node(
            interface,
            name=node_name,
        )

    # Function interface case
    if isinstance(interface.interface, niu.Function):
        # Get inputs
        ins = interface.inputs
        interface_dict = ins.get()
        building_blocks = interface_dict.keys()
        input_vars = []
        for element in building_blocks:
            if element == 'function_str':
                niu_function = interface_dict[element]
            else:
                input_vars.append(element)
            if element == 'imports':
                niu_imports = interface_dict[element]
            else:
                niu_imports = None

        # Get outputs
        outs = interface.outputs
        interface_dict = outs.get()
        building_blocks = interface_dict.keys()
        output_vars = []
        for element in building_blocks:
            output_vars.append(element)
        return pydra.mark.task(create_function_from_source(niu_function, imports=niu_imports))

    elif isinstance(interface.interface, bs.SimpleInterface):
        # Get inputs
        ins = interface.inputs
        interface_dict = ins.get()
        building_blocks = interface_dict.keys()
        input_vars = []
        for element in building_blocks:
            input_vars.append(element)
            # if element == 'imports':
            #     niu_imports = interface_dict[element]
            # else:
            #     niu_imports = None
        niu_function = interface.interface._run_interface.__func__

        # Get outputs
        outs = interface.outputs
        interface_dict = outs.get()
        building_blocks = interface_dict.keys()
        output_vars = []
        for element in building_blocks:
            output_vars.append(element)
        #return pydra.mark.task(create_function_from_source(niu_function, imports=niu_imports))
        return pydra.mark.task(niu_function)

    # Commandline interface case
    elif isinstance(interface.interface, bs.CommandLine):
        cmdline = interface.interface.cmdline.split(' ')
        sct = ShellCommandTask(name=interface.name, executable=cmdline)
        return sct
