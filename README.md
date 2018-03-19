# Image-Forgery-Detection
Detection of copy-move and splice forgeries in images using deep learning and diverse image representation methods

In this project, we propose a deep learning based technique for image forgery detection. We propse a model where the CNN automatically learns hierarchical relationships from the input RGB color images. The CNN architecture will be specifically designed for image splicing and copy-move detection applications.

The CNN models generally used in literature employ a large number of layers with each affine layer having an enormous number of hidden units, thereby making their application computationally expensive. We therefore propose a novel image representation method which extracts suitable features from images and constructs a low-dimensional representation of an image which is then fed to a CNN with lesser number of layers than the original model, thereby increasing making the algorithm computationally expensive.

The image representation works by first taking Discrete Wavelet Transform (DWT) of the forged input image and then performing Discrete Cosine Transform Quantization Coefficient Decomposition (DCT-QCD) on the bands obtained from DWT. The shift vectors so generated are then fed to a CNN to detect forgery regions in the input image.

We plan to evaluate our model on 3 public benchmark datasets for forgery detection: CASIA v1.0[4], CASIA v2.0[5] and Columbia Gray DVMM[6]. 

The following papers provide references to the ideas behind the above proposal:


[1]. T. T. Ng and S. F. Chang, "A model for image splicing," Image Processing, 2004. ICIP '04. 2004 International Conference on, 2004, pp. 1169-1172 Vol.2.

[2]. M. Ghorbani, M. Firouzmand and A. Faraahi, "DWT-DCT (QCD) based copy-move image forgery detection," 2011 18th International Conference on Systems, Signals and Image Processing, Sarajevo, 2011, pp. 1-4.

[3]. Y. Rao and J. Ni, "A deep learning approach to detection of splicing and copy-move forgeries in images," 2016 IEEE International Workshop on Information Forensics and Security (WIFS), Abu Dhabi, 2016, pp. 1-6.

[4]. T. K. Huynh, K. V. Huynh, Thuong Le-Tien and S. C. Nguyen, "A survey on Image Forgery Detection techniques," The 2015 IEEE RIVF International Conference on Computing & Communication Technologies - Research, Innovation, and Vision for Future (RIVF), Can Tho, 2015, pp. 71-76.

[5]. Wu, Yue; AbdAlmageed, Wael; Natarajan, Prem Deep Matching and Validation Network -- An End-to-End Solution to Constrained Image Splicing Localization and Detection
