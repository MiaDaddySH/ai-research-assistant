import 'dart:convert';

import 'package:http/http.dart' as http;

import '../models/research_response.dart';

class ApiService {
  ApiService();

  static const String _configuredBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: '',
  );
  static const String _defaultBaseUrl = 'http://127.0.0.1:8000';

  static String get _baseUrl {
    final resolvedBaseUrl = _configuredBaseUrl.isNotEmpty
        ? _configuredBaseUrl
        : _defaultBaseUrl;
    if (resolvedBaseUrl.endsWith('/')) {
      return resolvedBaseUrl.substring(0, resolvedBaseUrl.length - 1);
    }
    return resolvedBaseUrl;
  }

  Future<ResearchResponse> research(String question) async {
    final uri = Uri.parse('$_baseUrl/research');

    final response = await http.post(
      uri,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'question': question}),
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
