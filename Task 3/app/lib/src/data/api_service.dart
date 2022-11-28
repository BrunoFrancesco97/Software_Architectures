import 'dart:developer';
import 'dart:io';
import 'package:dio/dio.dart';
import 'dart:convert';

import 'course.dart';
import 'assignment.dart';
import 'constants.dart';

class ApiService {
  var api = Dio(
    BaseOptions(
      baseUrl: ApiConstants.baseUrl,
      connectTimeout: 5000,
      receiveTimeout: 3000
    )
  );

  Future login(mail, password) async {
    Codec<String, String> stringToBase64 = utf8.fuse(base64);
    String encoded_credentials =  stringToBase64.encode(mail+":"+password);
    try {
      var response = await api.get(
          ApiConstants.login,
        options: Options(
          headers: {
            "Authorization": "Basic "+encoded_credentials
          }
        )
      );
      log(response.toString());
      log(response.statusCode.toString());
      if(response.statusCode == 200)
        return true;
    } catch (e) {
      log(e.toString());
    }
  }

  Future test() async {
    //sleep(Duration(seconds: 1));
    log("test api call");
    return "test";
  }
}