echo "Installing packages from INIT"
#pip uninstall --yes refractio
#pip uninstall --yes pandas
python -m pip install --upgrade pip
pip install feast==0.34.1
pip install snowflake-snowpark-python==1.6.1
echo "Done with dependency installation!";