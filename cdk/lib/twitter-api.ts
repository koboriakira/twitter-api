/** @format */

import {
  Stack,
  StackProps,
  RemovalPolicy,
  Duration,
  aws_lambda as lambda,
  aws_iam as iam,
  aws_apigateway as apigateway,
  aws_s3 as s3,
} from "aws-cdk-lib";
import { Construct } from "constructs";
import { convertToCamelCase } from "./utils";

// CONFIG
const RUNTIME = lambda.Runtime.PYTHON_3_11;
const TIMEOUT = 30;
const APP_DIR_PATH = "../src";
const LAYER_ZIP_PATH = "../dependencies.zip";

export class TwitterApi extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    // S3バケットを作成
    const bucket = this.makeS3Bucket();

    const role = this.makeRole(bucket.bucketArn);
    const myLayer = this.makeLayer();

    // FastAPI(API Gateway)の作成
    const main = this.createLambdaFunction("fastapi_main", role, myLayer);
    this.makeApiGateway(main);
  }

  makeS3Bucket() {
    return new s3.Bucket(this, "Bucket", {
      bucketName: "twitter-api-bucket-koboriakira",
      removalPolicy: RemovalPolicy.DESTROY,
    });
  }

  /**
   * Create or retrieve an IAM role for the Lambda function.
   * @returns {iam.Role} The created or retrieved IAM role.
   */
  makeRole(
    bucketArn: string
  ) {
    // Lambdaの実行ロールを取得または新規作成
    const role = new iam.Role(this, "LambdaRole", {
      assumedBy: new iam.ServicePrincipal("lambda.amazonaws.com"),
    });

    // Lambda の実行ロールに管理ポリシーを追加
    role.addManagedPolicy(
      iam.ManagedPolicy.fromAwsManagedPolicyName(
        "service-role/AWSLambdaBasicExecutionRole"
      )
    );

    // 必要に応じて追加の権限をポリシーとしてロールに付与
    role.addToPrincipalPolicy(
      new iam.PolicyStatement({
        actions: ["lambda:InvokeFunction", "lambda:InvokeAsync"],
        resources: ["*"],
      })
    );

    role.addToPrincipalPolicy(
      new iam.PolicyStatement({
        actions: ["s3:*"],
        resources: [bucketArn, bucketArn + "/*"],
      })
    );

    return role;
  }

  /**
   * Create or retrieve a Lambda layer.
   * @returns {lambda.LayerVersion} The created or retrieved Lambda layer.
   */
  makeLayer() {
    return new lambda.LayerVersion(this, "Layer", {
      code: lambda.Code.fromAsset(LAYER_ZIP_PATH), // レイヤーの内容を含むディレクトリ
      compatibleRuntimes: [RUNTIME], // このレイヤーが互換性を持つランタイム
    });
  }

  /**
   * Create a Lambda function.
   * @param {iam.Role} role The IAM role for the Lambda function.
   * @param {lambda.LayerVersion} myLayer The Lambda layer to be used.
   * @returns {lambda.Function} The created Lambda function.
   */
  createLambdaFunction(
    handlerName: string,
    role: iam.Role,
    myLayer: lambda.LayerVersion,
    function_url_enabled: boolean = false,
    timeout: number = TIMEOUT
  ): lambda.Function {
    const resourceNameCamel = convertToCamelCase(handlerName);

    const fn = new lambda.Function(this, resourceNameCamel, {
      runtime: RUNTIME,
      handler: handlerName + ".handler",
      code: lambda.Code.fromAsset(APP_DIR_PATH),
      role: role,
      layers: [myLayer],
      timeout: Duration.seconds(timeout),
    });

    fn.addEnvironment("TWITTER_USER_NAME", process.env.TWITTER_USER_NAME || "");
    fn.addEnvironment("TWITTER_PASSWORD", process.env.TWITTER_PASSWORD || "");
    fn.addEnvironment("TWITTER_EMAIL_ADDRESS", process.env.TWITTER_EMAIL_ADDRESS || "");

    if (function_url_enabled) {
      fn.addFunctionUrl({
        authType: lambda.FunctionUrlAuthType.NONE, // 認証なし
      });
    }

    return fn;
  }

  /**
   * Create an API Gateway.
   * @param {lambda.Function} fn The Lambda function to be integrated.
   */
  makeApiGateway(fn: lambda.Function) {
    // REST API の定義
    const restapi = new apigateway.RestApi(this, "Twitter-Api", {
      deployOptions: {
        stageName: "v1",
      },
      restApiName: "Twitter-Api",
    });
    // ルートとインテグレーションの設定
    restapi.root.addMethod("ANY", new apigateway.LambdaIntegration(fn));
    restapi.root
      .addResource("{proxy+}")
      .addMethod("ANY", new apigateway.LambdaIntegration(fn));
    return restapi;
  }
}
