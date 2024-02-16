


# Lịch cúp nước

Notify when there are new water interruption
## Usage

### Deployment

Deploy infra
```
sls deploy --aws-profile <profile> --region <region> --param="chatid=<chat-id-value>" --param="token=bot<token-value>" -c serverless-infra.yml
```
Then deploy service
```
sls deploy --aws-profile <profile> --region <region>
```