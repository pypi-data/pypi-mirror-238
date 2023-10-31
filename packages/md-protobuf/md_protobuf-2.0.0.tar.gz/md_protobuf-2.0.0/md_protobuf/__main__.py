from md_protobuf.generator import document_file
from google.protobuf.descriptor import FieldDescriptor
from google.protobuf.descriptor_pb2 import FileOptions
from google.protobuf.compiler.plugin_pb2 import CodeGeneratorRequest, CodeGeneratorResponse
from sys import stdin, stdout, stderr

serialized = stdin.read()
request = CodeGeneratorRequest()
request.ParseFromString(serialized)

response = CodeGeneratorResponse()
ltag = ''

# each input file to the compiler
for i in range(0, len(request.proto_file)):
    file_descriptor = request.proto_file[i]
    filename = file_descriptor.name
    package = file_descriptor.package

    if file_descriptor.options.optimize_for == FileOptions.LITE_RUNTIME:
        ltag = 'Lite'

    # for now, we require package, which is bad
    # TODO fix this
    if not package:
        response.error = 'file seen without package. md-protobuf currently requires a package on every proto file: %s' % filename
        break

    define_value = package.replace('.', '_').upper()
    cpp_header = '%s.pb.h' % package.replace('.', '/')
    cpp_namespace = '::%s' % package.replace('.', '::')

    f = response.file.add()
    f.name = '%s.md' % package.replace('.', '/').lower()
    f.content = document_file(file_descriptor)

stdout.write(response.SerializeToString())
exit(0)

