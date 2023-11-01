echo "Installing packages from INIT"
pip uninstall --yes refractio
#pip uninstall --yes pandas
pip install feast==0.34.1
#pip install jsonpickle==3.0.2
pip install snowflake-snowpark-python==1.6.1
echo "Done with dependency installation!";