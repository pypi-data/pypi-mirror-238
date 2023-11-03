## **AlphafoldModel** is a package to parse Alphafold PDB structures and PAE Matrices into interactive Python objects.

### The package contains the following classes:
- `AlphafoldModel`: Parses the Alphafold model PDB file alongside its JSON PAE matrix into an interactive Python object. It allows declarative queries for a model's local PAE and plDDT metrics.
- `ModelPDB`: `ModelPDB` is the base class that carries the PDB parsing functionalities as well as residue-based nearest-neighbour search methods.
- `ModelPAE`: `ModelPAE` is the base class that carries the PAE parsing functionalities for `AlphafoldModel`.
- `LoadedKDTree`: `LoadedKDTree` is a wrapper class which provides an interface over the `scipy.spatial.KDTree` class to instead store and return arbitrary objects with coordinate information.

### Explore the source file in:
`src/AlphafoldModel/alphafoldmodel`
