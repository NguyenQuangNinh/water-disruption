


# Lịch cúp nước (Water disruption plan)

Notify Telegram users when there are new water outages
## Usage

### Deployment

Deploy infra
```
sls deploy --aws-profile <profile> --region <region> --param="chatid=<chat-id-value>" --param="token=bot<token-value>" --param="email=<email>" -c serverless-infra.yml
```
Then deploy service
```
sls deploy --aws-profile <profile> --region <region>
```
## System design
![Architecture Diaram](diagram.png)