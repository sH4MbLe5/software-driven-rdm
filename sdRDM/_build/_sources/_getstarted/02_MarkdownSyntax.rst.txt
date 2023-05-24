.. raw:: html

   <h2 align="center">

Markdown Example for sdRDM

.. raw:: html

   </h2>

.. raw:: html

   <p align="center">

This is an example of how to set up a data model using the
Software-Driven Research Data Management (sdRDM) library which is based
on abstract object models. Furthermore, the sdRDM library supports the
conversion of data models defined in the Markdown format to python
objects.

.. raw:: html

   </p>

The data model defined in the Markdown format is structured by using
different heading levels from 1 to 3.The following conventions are used:

.. raw:: html

   <h3>

Heading structure

.. raw:: html

   </h3>

-  The **Title of the data model** is denoted by a heading level 1 ``#``
   and is the root element of the data model.
-  **Object groups** are denoted by a heading level 2 ``##`` and can
   comprise multiple **Objects**.
-  **Enumerations** is denoted by a heading level 2 ``##`` as well and
   holds all the **Enumeration Objects**.

Note, that **Object group** classes can be named arbitrarily and
multiple are allowed, while only one **Enumerations** class is allowed
and it is required to have the name **Enumerations**.

-  The individual **Objects** are started with a heading level 3 ``###``
   and are gathered under a **Object group** heading level 2.
-  **Enumerations** are started with a heading level 3 ``###`` as well
   and are gathered under the **Enumerations** heading level 2.

.. raw:: html

   <h3>

Attributes

.. raw:: html

   </h3>

-  Each **object** contains **attributes** as a list → ``- attribute``
   which describe the object.
-  Attributes of an **Enumeration Object** are gathered between a triple
   apostrophe and a tailing ‘python’ → \```python an end with a triple
   apostrophe → \``\`
-  **Required attributes** are denoted with a double underscore →
   ``- __attribute__``
-  Each field has **options** as a list of name to value mapping →
   ``- Type: string``
-  In order to create an **inheritance** of attributes to another
   object, the object definition additionally includes the name of the
   parent object in italic wrapped with brackets →
   ``### Object [_ParentObject_]``

.. raw:: html

   <h3>

Properties

.. raw:: html

   </h3>

Each attribute in an object can hold multiple properties relevant for
mapping to another data model (e.g. a standardized format) and general
information such as its type and description. In the following is a
collection of all native and required properties:

-  **Type** - Required property to denote the data type. Multiple data
   types are allowed and can be denoted as a list or seperated by
   commata. Please note in particuar, that they can also be other
   objects defined in this document. To keep a better overview,
   especially in comprehesive markdown files, links can be set that
   point to the corresponding **Object** by denoting their name in
   parantheses. → ``(object name)``. The data types available besides
   **Objects** are as a list at the bottom line:

-  **Multiple** - Whether or not this attribute can contain multiple
   values. Setting to ``True`` will result in a ``List[dtype]``
   annoatation in the software.

-  **Description** - Required option to describe the attribute. This
   should be a brief description that explains what the attribute is
   about.

-  **References** - Optional property to create a reference to foo.

-  **XML** - Optional property to bar.

In the following an example data model is defined using above rules.
Feel free to use this example also as a template for your own
application.

--------------

Biocatalyst
===========

Do fugiat mollit sit duis deserunt dolor ex. Quis do occaecat dolor
consectetur nostrud occaecat eu sint aute. Laboris commodo laborum
proident id laboris cupidatat amet commodo tempor laborum sint occaecat
mollit velit.

Objects
-------

BiocatalystBase
~~~~~~~~~~~~~~~

Do fugiat mollit sit duis deserunt dolor ex. Quis do occaecat dolor
consectetur nostrud occaecat eu sint aute. Laboris commodo laborum
proident id laboris cupidatat amet commodo tempor laborum sint occaecat
mollit velit.

-  name

   -  Type: string
   -  Description: Name of the biocatalyst

-  ecnumber

   -  Type: string
   -  Description: Code used to determine the family of a protein.

-  reaction

   -  Type: string
   -  Description: Reaction in which the biocatalyst is activ.

-  sequence

   -  Type: string
   -  Description: Amino acid sequence of the biocatalyst.

-  host_organism

   -  Type: string
   -  Description: Organism used for expression.

-  source_organism

   -  Type: string
   -  Description: Organism the biocatalyst originates from.

-  post_translational_mods

   -  Type: string
   -  Description: Post-translational modifications that were made.

-  production_procedure

   -  Type: string
   -  Description: Procedure on how the biocatalyst was
      synthesized/expressed.

-  isoenzyme

   -  Type: string
   -  Description: Isoenzyme of the biocatalyst.

-  tissue

   -  Type: string
   -  Description: Tissue in which the reaction is happening.

-  localisation

   -  Type: string
   -  Description: Localisation of the biocatalyst.

SolubleBiocatalyst [*BiocatalystBase*]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Irure dolore dolore non sit adipisicing anim commodo est laborum.
Proident do do velit eiusmod. Amet aliquip mollit aliqua voluptate eu.
Proident ut id Lorem fugiat fugiat cillum ex. Aliqua excepteur laborum
quis qui minim esse. Proident magna nostrud pariatur eiusmod nisi
excepteur cillum sunt ad deserunt sint culpa ut proident. Esse ex qui
occaecat aliquip ipsum exercitation amet ullamco laborum ea commodo
exercitation do.

-  storage

   -  Type: StorageConditions
   -  Multiple: True
   -  Description: How the soluble biocatalyst has been stored.

-  concentration

   -  Type: posfloat
   -  Description: Concentration of the biocatalyst.

-  concentration_det_method

   -  Type: string
   -  Description: Method on how the concentration has been determined.

ImmobilisedCatalyst [*SolubleBiocatalyst*]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Laboris aliquip cupidatat id aliqua magna. Minim consectetur enim dolor
qui laborum aute nisi. Sit quis aute aliquip labore anim quis consequat
consequat anim nulla consequat in Lorem. Fugiat cupidatat nostrud
nostrud enim in. Proident in fugiat excepteur elit quis laboris nostrud
veniam cillum elit culpa. Excepteur qui irure ipsum eu. Officia
exercitation ut dolor anim nulla Lorem ut incididunt amet aute do.

-  purification

   -  Type: string
   -  Description: How the biocatalyst was purified.

-  immobilisation_procedure

   -  Type: string
   -  Description: How the biocatalyst was immobilised

CrudeCellExtract [*SolubleBiocatalyst*]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fugiat fugiat nulla mollit officia exercitation adipisicing et labore
proident nostrud proident fugiat. Voluptate esse mollit nulla tempor
proident laborum et voluptate eu sit commodo. Elit consequat consectetur
excepteur nulla irure qui. Proident labore esse ipsum Lorem eiusmod
labore tempor consequat est esse deserunt. Fugiat aliqua sit tempor
incididunt qui.

-  cell_disruption_process

   -  Type: string
   -  Description: Method used to disrupt cells.

-  purity_determination

   -  Type: string
   -  Description: Method that was used to determine the purity of the
      extract.

WholeCell [*BiocatalystBase*]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fugiat dolor enim aute dolore tempor consectetur commodo commodo
occaecat pariatur aute. Incididunt aliqua do ipsum proident do aute
cupidatat tempor voluptate mollit eiusmod sunt. Quis duis mollit anim ex
nulla enim minim. Incididunt qui commodo cupidatat occaecat dolor ipsum
excepteur sint fugiat minim. Enim ipsum adipisicing ut proident enim
sunt non.

-  harvesting_method

   -  Type: string
   -  Description: How the cells were harvested.

StorageConditions
~~~~~~~~~~~~~~~~~

Ut aute ut Lorem veniam proident. Laborum do nisi ut eiusmod in nostrud
proident. Commodo nulla ipsum commodo culpa aliqua dolore. Labore
exercitation eiusmod ea do tempor. Eiusmod enim mollit sit enim eiusmod
anim excepteur veniam culpa minim dolor. Labore aliquip sint laboris
quis mollit nostrud cillum dolore elit sunt pariatur aliquip.

-  temperature

   -  Type: float
   -  Description: Temperature at which the enzyme is stored.

-  storing_start

   -  Type: date
   -  Description: Date when catalyst was put into storage.

-  removing

   -  Type: date
   -  Description: Date when catalyst was removed from storage.

-  rethawing

   -  Type: date
   -  Description: Date when catalyst was rethawed from storage.

-  thawing_process

   -  Type: date
   -  Description: Method of thawing.

Enumerations
------------

Units
~~~~~

.. code:: python

   MOLPERLITER = 'mol / L'
   KELVIN = 'K'

str, string, float, int, integer, bytes, Email, Str, Email, HttpUrl,
HttpURL, httpurl, AnyHttpUrl, AnyHttpURL, anyhttpurl, AnyUrl, URL,
posfloat, PositiveFloat, positivefloat, date, datetime, bool, boolean,
Decimal, decimal, Enum, enum, Path, path, Any, any, Callable, callable,
FrozenSet, frozenset, Optional, optional, Pattern, pattern, UUID, uuid,
NoneStr, nonestr, NoneBytes, nonebytes, StrBytes, strbytes,
NoneStrBytes, nonestrbytes, OptionalInt, optionalint, OptionalIntFloat,
optionalintfloat, OptionalIntFloatDecimal, optionalintfloatdecimal,
StrIntFloat, strintfloat, StrictBool, strictbool, PositiveInt,
positiveint, NegativeInt, negativeint, NonPositiveInt, nonpositiveint,
NonNegativeInt, nonnegativeint, StrictInt, strictint, ConstrainedFloat,
constrainedfloat, NegativeFloat, negativefloat, NonPositiveFloat,
nonpositivefloat, NonNegativeFloat, nonnegativefloat, StrictFloat,
strictfloat, StrictBytes, strictbytes, StrictStr, strictstr, UUID1,
uuid1, UUID3, uuid3, UUID4, uuid4, UUID5, uuid5, FilePath, filepath,
DirectoryPath, directorypath, Json, json, PastDate, pastdate,
FutureDate, futuredate, NDArray, ndarray, ndArray, H5Dataset, h5dataset.
