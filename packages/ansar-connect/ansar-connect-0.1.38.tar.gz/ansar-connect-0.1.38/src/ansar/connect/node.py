# Author: Scott Woods <scott.18.ansar@gmail.com.com>
# MIT License
#
# Copyright (c) 2017-2023 Scott Woods
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
__docformat__ = 'restructuredtext'

import ansar.create as ar
from .socketry import *
from .directory import *

__all__ = [
	'create_node',
]

#
#
def node_parameters(specific_settings):
	if specific_settings is not None:
		a = ar.object_settings.__art__.value.keys()		# Framework values.
		b = node_settings.__art__.value.keys()			# Node values.
		c = specific_settings.__art__.value.keys()		# Application.
		d = (set(a) | set(b)) & set(c)
		if len(d) > 0:
			j = ', '.join(d)
			raise ValueError('collision in settings names - {collisions}'.format(collisions=j))

	executable, word, ls = ar.command_args()
	x1, r1 = ar.extract_args(ar.object_settings, ls, None)
	x2, r2 = ar.extract_args(node_settings, r1, specific_settings)
	ar.arg_values(ar.object_settings, x1)
	ar.arg_values(node_settings, x2)
	return executable, word, r2

def create_node(object_type,
	factory_settings=None, factory_input=None, factory_variables=None,
	upgrade=None, logs=ar.log_to_nowhere):

	ar.create_object(object_type,
		factory_settings=factory_settings, factory_input=factory_input, factory_variables=factory_variables,
		upgrade=upgrade, logs=logs,
		parameter_passing=node_parameters)
