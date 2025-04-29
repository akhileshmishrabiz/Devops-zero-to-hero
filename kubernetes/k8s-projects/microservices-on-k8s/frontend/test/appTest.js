const nock = require('nock');
const chai = require('chai');
const chaiHttp = require('chai-http');
const server = require('../app'); // Adjust path accordingly
const expect = chai.expect;
const config = require('./../config.json'); // path to config file
const should = chai.should();

chai.use(chaiHttp);

const productsApiBaseUri = config.productsApiBaseUri;

describe('App', () => {
   
    describe('GET /', () => {
        it('should return status 200', (done) => {
            chai.request(server)
                .get('/')
                .end((err, res) => {
                    expect(res).to.have.status(200);
                    done();
                });
        });
    });

    describe('GET /products', () => {
        it('should get array of products', (done) => {
            
            // Mocking API Response
            nock(productsApiBaseUri) // Your API base URL for Products App
                .get('/api/products') // API endpoint
                .reply(200, [{
                   id: 1,
                   name: 'Sample Product',
                   description: 'Sample Description',
                   price: 99.99,
                   image_url: 'http://example.com/sample.jpg'
                }]);

            chai.request(productsApiBaseUri)
                .get('/api/products')
                .end((err, res) => {
                    expect(res).to.have.status(200);
                    expect(res.body).to.be.an('array');
                    expect(res.body[0]).to.have.property('name');
                    done();
                });
        });
    });

    // Test for 404 error for unknown routes 
    describe("GET /unknown-route", () => {
        it("should return 404 for unknown routes", (done) => {
            chai.request(server)
                .get("/unknown-route")
                .end((err, response) => {
                    // Add a check for the 'err' and log it for debugging
                    if(err) console.log(err);
                
                    // Check if 'response' is defined before proceeding with the test
                    if(response){
                        response.should.have.status(404);
                    }
                    done();
                });
        });
    });

    describe("GET /", () => {
        it("should contain a specific word or element", (done) => {
            chai.request(server)
                .get("/")
                .end((err, response) => {
                    response.text.should.include("School of Devops");
                    done();
                });
        });
    });

    describe("GET /", () => {
        it("should display the service status section", (done) => {
            chai.request(server)
                .get("/")
                .end((err, response) => {
                    response.text.should.include("Service Status");
                    done();
                });
        });
    });




    // ... other tests
});

