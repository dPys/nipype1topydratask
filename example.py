#!/usr/env python

# Case 1: Function interface
# Old
def add_var(a, b):
    import pandas as pd
    return a + b

old_school_add_var_node = pe.Node(
    niu.Function(
        input_names=["a", "b"],
        output_names=["out"],
        function=add_var,
        imports=['import numpy as np'],
    ),
    name="old_school_add_var",
)

old_school_add_var_node.inputs.a = 4
old_school_add_var_node.inputs.b = 5

out = old_school_add_var_node.run()

# New
out_func_task = Nipype1topydratask(old_school_add_var_node)


# Case 2: Cmdline interface
# Old
from nipype.interfaces import afni
test_file = '/Users/derekpisner/Downloads/t1w_in_dwi.nii.gz'
calc = afni.Calc()
calc.inputs.in_file_a = test_file
calc.inputs.expr='step(a)'
calc.inputs.out_file =  'test_file_step_calc.nii.gz'
calc.inputs.outputtype = 'NIFTI'

# New
out_shell_task = Nipype1topydratask(calc)
