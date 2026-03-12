import 'package:flutter/material.dart';

import '../models/research_response.dart';
import '../services/api_service.dart';

class ResearchScreen extends StatefulWidget {
  const ResearchScreen({super.key});

  @override
  State<ResearchScreen> createState() => _ResearchScreenState();
}

class _ResearchScreenState extends State<ResearchScreen> {
  final TextEditingController _questionController = TextEditingController();
  final ApiService _apiService = ApiService();

  bool _isLoading = false;
  String? _errorMessage;
  ResearchResponse? _result;

  Future<void> _submitResearch() async {
    final question = _questionController.text.trim();

    if (question.isEmpty) {
      setState(() {
        _errorMessage = 'Please enter a research question.';
      });
      return;
    }

    setState(() {
      _isLoading = true;
      _errorMessage = null;
      _result = null;
    });

    try {
      final result = await _apiService.research(question);

      setState(() {
        _result = result;
      });
    } catch (e) {
      setState(() {
        _errorMessage = e.toString();
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  void dispose() {
    _questionController.dispose();
    super.dispose();
  }

  Widget _buildResult(ResearchResponse result) {
    return Expanded(
      child: ListView(
        children: [
          const SizedBox(height: 16),
          const Text(
            'Final Summary',
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 8),
          Text(result.summary),
          const SizedBox(height: 24),
          const Text(
            'Key Points',
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 8),
          ...result.keyPoints.map(
            (point) => Padding(
              padding: const EdgeInsets.only(bottom: 8),
              child: Text('• $point'),
            ),
          ),
          const SizedBox(height: 24),
          const Text(
            'Sources',
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 8),
          ...result.sources.map(
            (source) => Card(
              child: ListTile(
                title: Text(source.title),
                subtitle: Text(source.url),
              ),
            ),
          ),
          const SizedBox(height: 24),
          const Text(
            'Article Summaries',
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 8),
          ...result.articles.map(
            (article) => Card(
              child: Padding(
                padding: const EdgeInsets.all(12),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      article.title,
                      style: const TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      article.articleSummary,
                      style: const TextStyle(fontSize: 14),
                    ),
                  ],
                ),
              ),
            ),
          ),
          const SizedBox(height: 24),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('AI Research Assistant'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              controller: _questionController,
              decoration: const InputDecoration(
                labelText: 'Research Question',
                hintText: 'What are the latest developments in AI coding assistants?',
                border: OutlineInputBorder(),
              ),
              minLines: 1,
              maxLines: 3,
            ),
            const SizedBox(height: 12),
            SizedBox(
              width: double.infinity,
              child: FilledButton(
                onPressed: _isLoading ? null : _submitResearch,
                child: const Text('Research'),
              ),
            ),
            const SizedBox(height: 16),
            if (_isLoading) const CircularProgressIndicator(),
            if (_errorMessage != null) ...[
              Text(
                _errorMessage!,
                style: const TextStyle(color: Colors.red),
              ),
            ],
            if (_result != null) _buildResult(_result!),
          ],
        ),
      ),
    );
  }
}