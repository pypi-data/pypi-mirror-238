from lua_protobuf.generator import file_source, file_header, lua_protobuf_header, lua_protobuf_source
from google.protobuf.descriptor import FieldDescriptor
from google.protobuf.descriptor_pb2 import FileOptions
from google.protobuf.compiler.plugin_pb2 import CodeGeneratorRequest, CodeGeneratorResponse
from sys import stdin, stdout, stderr

serialized = stdin.buffer.read()
request = CodeGeneratorRequest()
request.ParseFromString(serialized)

response = CodeGeneratorResponse()
ltag = ''

# each input file to the compiler
for i in range(0, len(request.proto_file)):
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
        response.error = 'file seen without package. lua-protobuf currently requires a package on every proto file: %s' % filename
        break

    define_value = package.replace('.', '_').upper()
    cpp_header = '%s.pb.h' % target_name
    cpp_namespace = '::%s' % package.replace('.', '::')

    f = response.file.add()
    stderr.write('Generating : %s.pb-lua.h\n'%target_name)
    f.name = '%s.pb-lua.h' % target_name
    f.content = file_header(file_descriptor, target_name)

    f = response.file.add()
    stderr.write('Generating : %s.pb-lua.cc\n'%target_name)
    f.name = '%s.pb-lua.cc' % target_name
    f.content = file_source(file_descriptor, target_name, ltag)

f = response.file.add()
f.name = 'lua-protobuf.h'
f.content = lua_protobuf_header(ltag)

f = response.file.add()
f.name = 'lua-protobuf.cc'
f.content = lua_protobuf_source(ltag)

stdout.buffer.write(response.SerializeToString())
exit(0)

