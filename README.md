# intuit-project
## Command-Line Usage
* -i : path to folder containing images
* -gt : path to folder containing .gt files
* -o : output text file path, contains more detailed OCR results (stats per document)
```
python tesseract_test -i ground-truth-test -gt ground-truth-test
```
![results](https://github.com/thelandsquid/intuit-project/blob/master/results/ground_truth_test_results.JPG "Test Results")
## Default to Realistic Noise Data Set
```
python tesseract_test
```
![results](https://github.com/thelandsquid/intuit-project/blob/master/results/realistic_noise_testing_results.JPG "Test Results")
