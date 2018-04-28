# Image-Forgery-Detection
Detection of copy-move and splice forgeries in images using deep learning and diverse image representation methods

The forgery_detect folder contains the program code
The test_images folder should contain the images to be tested. (Each image as its original and fake copy)
The output_images folder is the directory where the images resulting from forgery detection will be placed
The image_dataset directory contains some sample images to test

To test an image, simply move the image file to the test_images directory

To execute the code:

1. Open a Terminal/Shell
2. Run the command -   python main.py
3. Enter the name of the image file when prompted, say "horse_fake.png" (without quotes)
4. The output images will be generated in the output_images directory


We plan to evaluate our model on 3 public benchmark datasets for forgery detection: CASIA v1.0[4], CASIA v2.0[5] and Columbia Gray DVMM[6]. 

The following papers provide references to the ideas behind the above proposal:

[1] M. Zimba, S. Xingming , “DWT-PCA (EVD) Based Copy-move Image Forgery Detection”, in International Journal of Digital Content Technology and its Applications , January 2011, PP. 251-258

[2]. T. T. Ng and S. F. Chang, "A model for image splicing," Image Processing, 2004. ICIP '04. 2004 International Conference on, 2004, pp. 1169-1172 Vol.2.

[3]. M. Ghorbani, M. Firouzmand and A. Faraahi, "DWT-DCT (QCD) based copy-move image forgery detection," 2011 18th International Conference on Systems, Signals and Image Processing, Sarajevo, 2011, pp. 1-4.

[4]. Y. Rao and J. Ni, "A deep learning approach to detection of splicing and copy-move forgeries in images," 2016 IEEE International Workshop on Information Forensics and Security (WIFS), Abu Dhabi, 2016, pp. 1-6.

[5]. T. K. Huynh, K. V. Huynh, Thuong Le-Tien and S. C. Nguyen, "A survey on Image Forgery Detection techniques," The 2015 IEEE RIVF International Conference on Computing & Communication Technologies - Research, Innovation, and Vision for Future (RIVF), Can Tho, 2015, pp. 71-76.

[6]. Wu, Yue; AbdAlmageed, Wael; Natarajan, Prem Deep Matching and Validation Network -- An End-to-End Solution to Constrained Image Splicing Localization and Detection
