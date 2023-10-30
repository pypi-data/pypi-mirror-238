import subprocess
import os

def install_package(package_name):
    command = f"pip install {package_name}"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if process.returncode == 0:
        return "Installation successful!"
    else:
        return f"Installation failed with error: {error.decode('utf-8')}"

def uninstall_package(package_name):
    command = f"pip install {package_name}"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    
    if process.returncode == 0:
        return "Installation successful!"
    else:
        return f"Installation failed with error: {output.decode('utf-8')}"

def run_it(command, input_data=None):
    process = subprocess.Popen(
        command.split(),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    try:
        if input_data is not None:
            process.stdin.write(input_data)
        process.stdin.flush()
        output, error = process.communicate()
        if output:
            Output= "Output: ```\n" + output +"```"
            return Output
        elif error:
            # print("Error:", error)
            Error = "Error: ```\n"+ error + "\n```err"
            return Error
    except Exception as e:
        print(e)

# def run_simp(cmd):
#     out = subprocess.run(cmd)
#     print(out)

# def run_ssmiip(command):
#     try:
#         subprocess.check_output(command, shell=True)
#         print("Download completed")
#     except subprocess.CalledProcessError as e:
#         print(f"Download failed error code as {e.returncode}")


# print(run_it("pip uninstall pySmartDL", "Y"))