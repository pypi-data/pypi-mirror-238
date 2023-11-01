# Introduction 

This repository was created to provide reusable tools for validating "double-runs" in the context of the Cockpit migration project, but also for other refactoring projects (MLOps, LACI, etc.).

# Usage

Install the `doublerun` package using `pip`:

In Databricks:

`%pip install doublerun` 

**If you are using an old databricks runtime and you use outdated `pandas` or `pyspark` versions, run this instead to avoid updating `pandas` and `pyspark` (at your own risk)**:

`%pip install --no-deps doublerun`

Locally:

`pip install --proxy http://127.0.0.1:3128 doublerun`


## Pandas Usage

Import the comparison functions:

```py
import pandas as pd
from doublerun.pandas import (
    comparison_count,
    comparison_schema,
    comparison_columns,
    comparison_records,
    global_comparison
)

df1 = pd.DataFrame({
        'Column1' : [1, 2, 3],
        'Column2' : ['A', 'B', 'C']
    })

df2 = pd.DataFrame({
    'Column1' : [1, 2, 3, 4],
    'Column3' : ['E', 'B', 'C', 'F']
})
```

### Compare the number of rows between the two DataFrames.

```py
df1_count, df2_count = comparison_count(df1, df2)
```

Output:
```
************************COMPARAISON DU NOMBRE DE LIGNES*************************

    Le nombre de lignes des deux DataFrames ne sont pas égaux :
        - Pour le DataFrame 1 on a 3 lignes.
        - Pour le DataFrame 2 on a 4 lignes.
```

### Compare the schema of the two DataFrames and return the missing columns in each.

```py
missing_cols_in_1, missing_cols_in_2 = comparison_schema(df1, df2)
```

Output:
```
*****************************COMPARAISON DU SCHEMA******************************

    Les schémas ne sont pas équivalents.
    Dans le DataFrame 1 il y a ces colonnes manquantes par rapport au DataFrame 2:
        ['Column3']
    
    Dans le DataFrame 2 il y a ces colonnes manquantes par rapport au DataFrame 1:
        ['Column2']
```

### Compare the number of columns in the two DataFrames and return the columns in common.

```py
common_columns = comparison_columns(df1, df2)
```

Output:
```
****************************COMPARAISON DES COLONNES****************************

    Le nombre de colonnes est identiques entre les deux DataFrames.
        Nombre de colonnes communes entre les deux DataFrames: 1
        Colonnes communes entre les deux DataFrames: 
            ['Column1']
```
### Compare the records of the two DataFrames and return:
 - common : Records present in both DataFrames.
 - left_only, right_only : Records present only in df1 or df2.

```py
common, left_only, right_only = comparison_records(df1, df2)
```

Output:
```        
***************COMPARAISON DES DONNÉES ENTRE LES DEUX DATAFRAMES****************

    Certaines lignes ne sont pas présentes dans les deux DataFrames:
            0 lignes sont uniquement dans le DataFrame 1.
            
            1 lignes sont uniquement dans le DataFrame 2.
            
            3 lignes sont présentes dans les deux DataFrames.
```

### Global Comparison

You can also run the `global_comparison` function and print all of the above at once.

```py
common, left_only, right_only = global_comparison(df1, df2)
```

# Spark Usage

Usage with `spark` DataFrames is exactly the same but functions need to be imported from **`doublerun.spark`** instead:

```py
import pandas as pd
from doublerun.spark import (
    comparison_count,
    comparison_schema,
    comparison_columns,
    comparison_records,
    global_comparison
)

df1 = pd.DataFrame({
        'Column1' : [1, 2, 3],
        'Column2' : ['A', 'B', 'C']
    })

df2 = pd.DataFrame({
    'Column1' : [1, 2, 3, 4],
    'Column3' : ['E', 'B', 'C', 'F']
})

df1 = spark.createDataFrame(df1)
df2 = spark.createDataFrame(df2)

comparison_count(df1, df2)
comparison_schema(df1, df2)
comparison_columns(df1, df2)
common, left_diff, right_diff = comparison_records(df1, df2)
# common, left_diff, right_diff = global_comparison(df1, df2)
```

# Contributing

In order to contribute, create your branch with a meaningful title representing a feature you would like to develop (Examples: `pandas_visualisation_mismatches`, `pandas_high_perf_dask`, `spark_notebooks`, etc.). Please, have a look at existing branches before creating a new one.

Then, make a pull request to the `dev` branch to make sure no conflicts are created when we will be merging multiple branches together.

# Credits

Thanks to Bilel BOUACHA of the HyperVision Team for providing the basis for the code contained in this package. This code was slightly refactored to be used as a general comparison tool between two `spark` or `pandas` DataFrames.