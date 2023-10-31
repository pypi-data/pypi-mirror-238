#!/usr/bin/env python

import os,subprocess,time,sys

##### Setup variables
tests_timeout=20 # Max duration of a test
tests_path = os.path.dirname(os.path.realpath(__file__))

##### Run all tests
for file in os.listdir(tests_path):
    current_test_path=os.path.join(tests_path,file)
    if os.path.isdir(current_test_path):
        platform_path=os.path.join(current_test_path,"platform.yaml")
        out_path=os.path.join(current_test_path,"out")
        print("- %-40s%s " % (file,"=>"),end='')
        try:
            start_at=time.time()
            out=subprocess.check_output(["esds", "run", platform_path],stderr=subprocess.STDOUT,timeout=tests_timeout,encoding="utf-8")
            out_expected=open(out_path).read()
            end_at=time.time()
            if out_expected != out:
                print("failed :(")
                print("------------- Expected -------------")
                print(out_expected,end="")
                print("------------- Got -------------")
                print(out,end="")
            else:
                print("passed (%0.1fs)"%(end_at-start_at))
        except subprocess.TimeoutExpired as err:
            print("failed :(")
            print("------------- Test duration expired (timeout="+str(tests_timeout)+"s) -------------")
            print(err.output,end="")
            exit(1)
        except subprocess.CalledProcessError as err:
            print("failed :(")
            print("------------- Test has a non-zero exit code -------------")
            print(err.output,end="")
            exit(2)
        except Exception as err:
            print("failed :(")
            print("Reason: "+str(err))
            exit(3)
