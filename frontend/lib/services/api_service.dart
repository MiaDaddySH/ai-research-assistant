import 'dart:convert';

import 'package:http/http.dart' as http;

import '../models/research_response.dart';

class ApiService {
  ApiService();

  // iOS Simulator:
  static const String _baseUrl = 'http://127.0.0.1:8000';

  // Android Emulator:
  // static const String _baseUrl = 'http://10.0.2.2:8000';

  //调用后端API进行研究
  Future<ResearchResponse> research(String question) async {
    final uri = Uri.parse('$_baseUrl/research');

    final response = await http.post(
      uri,
      headers: {
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'question': question,
      }),
    );

    if (response.statusCode != 200) {
      throw Exception(
        'Failed to fetch research result. '
        'Status code: ${response.statusCode}, body: ${response.body}',
      );
    }

    final Map<String, dynamic> json =
        jsonDecode(response.body) as Map<String, dynamic>;

    return ResearchResponse.fromJson(json);
  }
}