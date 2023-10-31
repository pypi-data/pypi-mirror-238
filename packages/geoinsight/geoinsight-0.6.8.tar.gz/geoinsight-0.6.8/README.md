# GeoInsight API python package

To get started with the GeoInsight API head over to [geoinsight.ai](https://dashboard.geoinsight.ai) and create an account. You will get an **GeoInsight Personal Token (GPT)** and an **API Private Key (APK)**.

## Install
To install the package just run a regular `pip install`


```
pip install geoinsight
```

Then import the package like this.

```
import geoinsight
```

The GeoInsight package come with an `api` class to access the endpoints and a `util` class with additional useful functions. You can initialize both like this:

```
api=geoinsight.api()
util=geoinsight.util()
```
The `api` class wraps all API endpoints in python functions and `util` is a collection of methods that are useful to end-users, such as getting from `r` to a geopandas dataframe `gdf`, or to get the custom `crs` spherical  map projection for any given `gdf`. The `api` class does not do any diagnostics, it is up to you and the context of your code to check if `r` comes back with a valid `200` http status code. Better write an `if` statement or a `try-catch` block if needed to check for `r.status`.

## Usage
Now use the **GeoInsight Personal Token (GPT)** and **API Private Key (APK)**.

```
api.set_access_token(_gpt='GPT',_apk='APK')
```
