# nyartbeatpkg
![Header](banner.png)
This is a package built for NY ArtBeat API 👋✨


## About the package 🎨
New York City, dubbed “the art capital of U.S.”, has an incredible amount of art events available on any given day. Given the huge volume of shows and exhibitions, it is often hard for people to filter through this mass data to find the event that interests them the most. With the API provided by the New York Art Beat, a platform that provides a comprehensive list of art events and reviews, this package first **incorporates the different event lists in a single dataset** and then **allows users to pinpoint their events of interest with a couple built-in search functions**.

The API is consists of **four categories** and **24 subcategories**, each has its own API in XML format. The database contains information on Name, Venue, Description, Image, Karma, Price, DateStart, DateEnd, PermanentEvent, Distance, Datum, Latitude, and Longitude (Children) of each Event (Parent). Some have missing values. The dataframe created by the function in this 
project follows the same structure as the API's.


## Installation ⚡

```bash
$ pip install nyartbeatpkg
```


## Usage 🤔

1. Query NY ArtBeat's API in XML format with specified structure
2. Retreive and create a dataframe concurred with the structure of the API
3. Use various functions provided in the package to
    1. transform and clean dataframe
    2. retrieve event info with a set of filters (i.e., Name, Media Genre, and Type of Events)
    3. retrieve a list events that are available that are currently available


## Contributing 💬

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.


## License 🔭

`nyartbeatpkg` was created by Ruiqi Xue. It is licensed under the terms of the MIT license.


## Credits 📫

`nyartbeatpkg` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
