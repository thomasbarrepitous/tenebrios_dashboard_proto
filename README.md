<h1 align="center">TenebriOS Dashboard</h1>

<p align="center">
  <img alt="Github top language" src="https://img.shields.io/github/languages/top/thomasbarrepitous/tenebrios_dashboard_proto?color=56BEB8">

  <img alt="Github language count" src="https://img.shields.io/github/languages/count/thomasbarrepitous/tenebrios_dashboard_proto?color=56BEB8">

  <img alt="Repository size" src="https://img.shields.io/github/repo-size/thomasbarrepitous/tenebrios_dashboard_proto?color=56BEB8">

  <img alt="License" src="https://img.shields.io/github/license/thomasbarrepitous/tenebrios_dashboard_proto?color=56BEB8">

  <img alt="Github issues" src="https://img.shields.io/github/issues/thomasbarrepitous/tenebrios_dashboard_proto?color=56BEB8" /> 

  <img alt="Github forks" src="https://img.shields.io/github/forks/thomasbarrepitous/tenebrios_dashboard_proto?color=56BEB8" />

  <img alt="Github stars" src="https://img.shields.io/github/stars/thomasbarrepitous/tenebrios_dashboard_proto?color=56BEB8" />
</p>

<!-- Status -->

<h4 align="center"> 
	🚧  TenebriOS 🚀 Under construction...  🚧
</h4> 

<hr>

<p align="center">
  <a href="#dart-about">About</a> &#xa0; | &#xa0; 
  <a href="#sparkles-features">Features</a> &#xa0; | &#xa0;
  <a href="#rocket-technologies">Technologies</a> &#xa0; | &#xa0;
  <a href="#white_check_mark-requirements">Requirements</a> &#xa0; | &#xa0;
  <a href="#checkered_flag-starting">Starting</a> &#xa0; | &#xa0;
  <a href="#memo-license">License</a> &#xa0; | &#xa0;
  <a href="https://github.com/thomasbarrepitous" target="_blank">Author</a>
</p>

<br>

## :dart: About ##

This project is a prototype for a flour beetle farming Weather Station. It is fed through an API dedicated for the TenebriOS project which will also be available under the MIT License.

## :sparkles: Features ##

:heavy_check_mark: Supports CO2, Temperature, Humidity;\
:heavy_check_mark: Point by point display;\
:heavy_check_mark: Average over time graph;\
:heavy_check_mark: Real time indicators;

## :rocket: Technologies ##

The following tools were used in this project:

- [Python](https://www.python.org/)
- [Dash](https://dash.plotly.com/)
- [Docker](https://www.docker.com/)

## :white_check_mark: Requirements ##

Before starting :checkered_flag:, you need to have [Git](https://git-scm.com) and [Docker](https://www.docker.com/) installed.

## :checkered_flag: Starting ##

```bash
# Clone this project
$ git clone https://github.com/thomasbarrepitous/tenebrios_dashboard_proto

# Access
$ cd tenebrios_dashboard_proto

# Build the Docker image
$ docker build -t tenebrios_dashboard .

# Run the container
$ docker run -p 8080:80 tenebrios_dashboard

# The server will initialize in the <http://localhost:8080>
```

## :memo: License ##

This project is under license from MIT. For more details, see the [LICENSE](LICENSE.md) file.


Made with :heart: by <a href="https://github.com/thomasbarrepitous" target="_blank">Thomas Barré-Pitous</a>

&#xa0;

<a href="#top">Back to top</a>
