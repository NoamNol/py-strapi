# Strapi for tests
Run it for PyStrapi integration tests

### Installation
```bash
npm ci
# or install and update (update package-lock):
npm install
```

### Prepare data
```
mkdir .tmp
cp testdata/data.db .tmp/
```


### Run
```
npm run develop
# or
npm run start
```

### More info:
**Admin user:**  
First name: `strapi`, Last name: `strapi`, Email: `strapi@test.com`, Password: `Strapi123`.
