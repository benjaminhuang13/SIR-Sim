# Frontend

_How to host webpage on S3_

1. Create bucket named `sir-sim.com`
2. Disable `Block all public access` in `Block Public Access settings for this bucket` and check the acknowledge warning message
3. Click `create` button
4. Go into the bucket and go into `Properties` tab
5. Scroll all the way down to `Static website hosting` and click `Edit`
6. Enable `Static website hosting`.
7. Select `Host a static website` for Hosting type.
8. Type `index.html` for Index document.
9. Click `Save changes`
10. Go to `Objects` tab and upload the `index.html` `sir-sim.js` `style.css` `favicon.png` `logo.png` files.

_How to create HTTP API Gateway_

1. Click `Create API`
2. Click `Build` under HTTP API. Wait for the creation and then open the API Gateway
3. Click `Create` next to `Routes for sirsim(name of api)`
4. Select `GET` for the route and type a path `sirsim/data`. Click `Create`
5. Do this again for PUT. Select `PUT` for the route and type a path `sirsim/data`. Click `Create`
6. Click on the `GET` route you just created. Click `Attach integration`.
7. Click `Create and attach an integration`. Select Lambda for `Integration target type`
8. Choose region `us-east-1` and search for the right lambda function.
9. Leave the `Grant API Gateway permission to invoke your Lambda function` enabled.

10. Go to `CORS` under `Develop`.
11. For Access-Control-Allow-Origin, add `*` and `http://sir-sim.com.s3-website-us-east-1.amazonaws.com/`.
12. For Access-Control-Allow-Methods, add `GET` and `POST`.
13. for Access-Control-Allow-Headers, add `content-type, origin, authorization, accept, x-requested-with, access-control-request-method, access-control-request-headers, access-control-allow-headers` (you can play around with this)
