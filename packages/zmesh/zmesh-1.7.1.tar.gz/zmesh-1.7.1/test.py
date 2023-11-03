import numpy as np
import zmesh

labels = np.zeros( (100, 100, 100), dtype=np.uint32)
labels[1:-1, 1:-1, 1:-1] = 1
labels[-5:,-5:,-5:] = 0

mesher = zmesh.Mesher( (1, 1, 1) )
mesher.mesh(labels)
mesh = mesher.get(1, normals=False, reduction_factor=0, max_error=10)

mesh.vertices += np.array([-30, 45, 60])

simplified = mesher.simplify(
  mesh,
  reduction_factor=100, 
  max_error=10,
)

print(mesh.vertices.shape, simplified.vertices.shape)
print(mesh.vertices.mean(axis=0), simplified.vertices.mean(axis=0))
print(mesh.vertices.min(axis=0), simplified.vertices.min(axis=0))

with open('simplified.obj', 'bw') as f:
  f.write(simplified.to_obj())

with open('unsimplified.obj', 'bw') as f:
  f.write(mesh.to_obj())

