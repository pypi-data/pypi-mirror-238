from cx_Freeze import setup, Executable
import os

# Determine the current directory and your main Python script
current_dir = os.path.dirname(os.path.realpath(__file__))
app_dir = os.path.join(current_dir, 'app.py')

# Get the requirements from requirements.txt in the previous directory
with open(os.path.join(current_dir, '..', 'requirements.txt')) as f:
    requirements = f.read().splitlines()

executables = [Executable(\
    script=app_dir,  # Use the app_dir variable as the script path
    base="Console",
)]

options = {
    "build_exe": {
        "packages": [],  # Replace with the package(s) your app uses
    }
}

setup(
    name="TypeBuild",
    version="1.0",
    description="A simple Mac App",
    options=options,
    executables=executables
)




# from cx_Freeze import setup, Executable
# import os
# current_dir = os.path.dirname(os.path.realpath(__file__))
# app_dir = os.path.join(current_dir, 'app.py')

# setup(
#     name="Typebuild",
#     version="1.0",
#     description="Your Streamlit-based app",
#     executables=[Executable(app_dir)],
#     options={
#         "build_exe": {
#             "packages": ['stqdm'],  # Include the Streamlit package
#         },
#     },
# )

