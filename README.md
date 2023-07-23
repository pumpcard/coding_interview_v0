# Liquidity Rank Service

## Usage

#### Prerequsites

```
poetry shell
```

#### Start the api service (in reload mode)

```
uvicorn server:app --reload
```

#### Dump AWS Reserved Instance Offerings

Currently hardcoded to `us-east-1` and `a1.2xlarge` instances

```
python aws-rios-to-json.py > us-east-1.json
```

## TODO

- [x] Get a FastAPI server running
- [x] Get an aws api interface working
- [ ] Get a db interface working
- [ ] Sketch architecture
