# EPR imaging toolkit
The EPR Imaging Toolkit is a set of tools for reconstructing and visualizing EPR images measured with the Bruker Elexsys E540 L-band tomograph. The toolkit supports the deconvolution of the projection with non-gradient spectrum, 
angular interpolation, and reconstruction of 2D, 3D, 3DS, and 4D images. It also provides tools for visualizing the obtained images.

### Installation
To install the EPR Imaging Toolkit, clone the repository and install the dependencies using pip:

### Configuration
All parameters can be set in configuration/config.json. Alternatively, you can edit the default configuration file configuration/default_config.json.

### Usage
To run the toolkit, navigate to the EPR Imaging Toolkit directory and run the following command:

Copy code
python -m epri_toolkit.run_local
This will use the default configuration file (configuration/default_config.json).

Alternatively, you can specify a custom configuration file by providing its path as a command-line argument:




Contributions
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or a pull request on GitHub.