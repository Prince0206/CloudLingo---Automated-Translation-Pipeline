# **CloudLingo – AWS Translate Automation**

**Region**: us-east-1 

**Author**: Prince Larbi Wireko 

**Description**: An automated translation pipeline using AWS S3, Lambda, and Amazon Translate. Upload a JSON file to the request bucket, and get a translated JSON in the response bucket — no manual intervention.



#### 📌 **Features**

**Serverless**: Fully managed with AWS Lambda and S3 triggers.



**Multi-language**: Supports any language pair supported by Amazon Translate.



**Automated**: Upload → Translate → Output in seconds.



**Versioned \& Managed**: S3 versioning and lifecycle rules for cost optimization.



#### **🛠 Architecture Overview**

Code

\[User Upload]

&nbsp;     |

&nbsp;     v

\[Request S3 Bucket] --(S3 Event)--> \[AWS Lambda] --> \[Amazon Translate]

&nbsp;     |                                                   |

&nbsp;     v                                                   v

\[Response S3 Bucket] <---------------------------------- Translated JSON



#### 📊 **AWS‑Icon Architecture Diagram**

![alt text](architecture.drawio.png)

#### **💻 Tech Stack**

**!\[AWS S3]**(https://img.shields.io/badge/AWS%20S3-569A31?style=for-the-badge\&logo=amazon-s3\&logoColor=white)

**!\[AWS Lambda](**https://img.shields.io/badge/AWS%20Lambda-FF9900?style=for-the-badge\&logo=awslambda\&logoColor=white**)**

**!\[Amazon Translate](**https://img.shields.io/badge/Amazon%20Translate-FFCB2B?style=for-the-badge\&logo=amazonaws\&logoColor=black**)**

**!\[Python](**https://img.shields.io/badge/Python-3776AB?style=for-the-badge\&logo=python\&logoColor=white**)**

**!\[CloudFormation](**https://img.shields.io/badge/AWS%20CloudFormation-FF4F8B?style=for-the-badge\&logo=amazonaws\&logoColor=white**)**





#### **🚀 Quick Start (Cheat Sheet)**

1\. **Deploy Infrastructure**

bash

aws cloudformation deploy \\

&nbsp; --stack-name cloudlingo \\

&nbsp; --template-file infra.yaml \\

&nbsp; --capabilities CAPABILITY\_NAMED\_IAM \\

&nbsp; --parameter-overrides BucketBaseName=cloudlingo-prince-2025-0902 \\

&nbsp; --region us-east-1

2\. **Get Resource Names**

bash

aws cloudformation describe-stacks \\

&nbsp; --stack-name cloudlingo \\

&nbsp; --region us-east-1 \\

&nbsp; --query "Stacks\[0].Outputs"



#### **📂 Project Structure**

Code

.

├── infra.yaml               # CloudFormation template

├── translate\_lambda.py      # Lambda handler

├── translate\_local.py       # Local test script

├── request\_en\_fr.json       # Sample request

├── assets/

│   └── architecture.png     # AWS-icon diagram

└── README.md                # This file



#### **🧪 Local Testing (Optional)**

**1. Create a request JSON**



json

{

&nbsp; "sourceLanguageCode": "en",

&nbsp; "targetLanguageCode": "fr",

&nbsp; "texts": \["Hello, world!", "How are you today?"],

&nbsp; "metadata": {"requestId": "demo-001"}

}



**2. Run the script**



bash

python translate\_local.py request\_en\_fr.json <RequestBucketName> <ResponseBucketName>

3\. Verify output



bash

aws s3 ls s3://<ResponseBucketName>/translated/ --region us-east-1

aws s3 cp s3://<ResponseBucketName>/translated/request\_en\_fr\_to\_fr.json . --region us-east-1



#### **⚡ Automated Lambda Flow**

1. Upload JSON to Request Bucket (prefix: inbox/ if configured).
2. 
3. S3 event triggers Lambda.
4. 
5. Lambda calls Amazon Translate.
6. 
7. Output JSON saved to Response Bucket.



#### **🛠 Debugging**

AWS Console → CloudWatch Logs → /aws/lambda/cloudlingo-translate



Check for:



* Permission errors
* 
* Wrong bucket names
* 
* Missing prefixes



#### **🧹 Cleanup**

bash

aws s3 rm s3://<RequestBucketName> --recursive --region us-east-1

aws s3 rm s3://<ResponseBucketName> --recursive --region us-east-1

aws cloudformation delete-stack --stack-name cloudlingo --region us-east-1



#### **💡 Next Steps**

* Add a simple web UI for uploads (S3 static site + API Gateway).
* 
* Batch process multiple files via SQS.
* 
* Tag S3 objects with language codes for easy filtering.
