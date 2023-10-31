from json_protobuf.generator import file_source, file_header, file_exception
from google.protobuf.descriptor import FieldDescriptor
from google.protobuf.descriptor_pb2 import FileOptions
from google.protobuf.compiler.plugin_pb2 import CodeGeneratorRequest, CodeGeneratorResponse
from sys import stdin, stdout, stderr

serialized = stdin.buffer.read()
request = CodeGeneratorRequest()
request.ParseFromString(serialized)

response = CodeGeneratorResponse()
ltag = ''

f = response.file.add()
f.name = 'exception.pb-json.h'
f.content = file_exception()

# each input file to the compiler
for i in range(0, len(request.proto_file)):
  try:
    file_descriptor = request.proto_file[i]
    if file_descriptor.name not in request.file_to_generate:
        continue
    filename = file_descriptor.name
    package = file_descriptor.package
    target_name = filename.replace('.proto', '').lower()

    if file_descriptor.options.optimize_for == FileOptions.LITE_RUNTIME:
        ltag = 'Lite'

    # for now, we require package, which is bad
    # TODO fix this
    if not package:
        response.error = 'file seen without package. json-protobuf currently requires a package on every proto file: %s' % filename
        break

    define_value = package.replace('.', '_').upper()
    cpp_header = '%s.pb.h' % target_name
    cpp_namespace = '::%s' % package.replace('.', '::')

    f = response.file.add()
    f.name = '%s.pb-json.h' % target_name
    f.content = file_header(file_descriptor, target_name)
    stderr.write('Generating : %s.pb-json.h\n'%target_name)

    f = response.file.add()
    f.name = '%s.pb-json.cc' % target_name
    f.content = file_source(file_descriptor, target_name, ltag)
    stderr.write('Generating : %s.pb-json.cc\n'%target_name)
  except e:
    stderr.write('Failed to generate %s: %s\n'%(package, e))


stdout.buffer.write(response.SerializeToString())
exit(0)
