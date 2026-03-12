import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

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

  static const List<String> _exampleQuestions = [
    'What are the latest developments in AI coding assistants?',
    'How are AI agents changing software engineering workflows?',
    'What are the recent trends in open-source large language models?',
  ];

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
        _errorMessage = 'Something went wrong:\n$e';
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  Future<void> _openUrl(String url) async {
    final uri = Uri.tryParse(url);
    if (uri == null) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Invalid URL')),
      );
      return;
    }

    final success = await launchUrl(uri, mode: LaunchMode.externalApplication);
    if (!success && mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Could not open link')),
      );
    }
  }

  void _applyExampleQuestion(String question) {
    setState(() {
      _questionController.text = question;
      _errorMessage = null;
    });
  }

  Widget _buildInputCard() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Research Question',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _questionController,
              minLines: 2,
              maxLines: 4,
              decoration: const InputDecoration(
                hintText: 'What are the latest developments in AI coding assistants?',
                border: OutlineInputBorder(),
              ),
              onSubmitted: (_) {
                if (!_isLoading) {
                  _submitResearch();
                }
              },
            ),
            const SizedBox(height: 12),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: _exampleQuestions
                  .map(
                    (question) => ActionChip(
                      label: Text(question),
                      onPressed: () => _applyExampleQuestion(question),
                    ),
                  )
                  .toList(),
            ),
            const SizedBox(height: 12),
            SizedBox(
              width: double.infinity,
              child: FilledButton.icon(
                onPressed: _isLoading ? null : _submitResearch,
                icon: const Icon(Icons.search),
                label: const Text('Start Research'),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildLoadingCard() {
    return const Card(
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Row(
          children: [
            SizedBox(
              width: 24,
              height: 24,
              child: CircularProgressIndicator(strokeWidth: 3),
            ),
            SizedBox(width: 16),
            Expanded(
              child: Text(
                'Research in progress... searching, reading sources, and generating a summary.',
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildErrorCard(String message) {
    return Card(
      color: Colors.red.shade50,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Icon(Icons.error_outline, color: Colors.red.shade700),
            const SizedBox(width: 12),
            Expanded(
              child: Text(
                message,
                style: TextStyle(color: Colors.red.shade900),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildEmptyState() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          children: [
            Icon(
              Icons.auto_awesome,
              size: 40,
              color: Theme.of(context).colorScheme.primary,
            ),
            const SizedBox(height: 12),
            Text(
              'Ask a question to generate an AI-powered research summary.',
              style: Theme.of(context).textTheme.bodyLarge,
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSectionCard({
    required String title,
    required Widget child,
  }) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(title, style: Theme.of(context).textTheme.titleLarge),
            const SizedBox(height: 12),
            child,
          ],
        ),
      ),
    );
  }

  Widget _buildSummaryCard(ResearchResponse result) {
    return _buildSectionCard(
      title: 'Final Summary',
      child: Text(
        result.summary,
        style: Theme.of(context).textTheme.bodyLarge,
      ),
    );
  }

  Widget _buildKeyPointsCard(ResearchResponse result) {
    return _buildSectionCard(
      title: 'Key Points',
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: result.keyPoints
            .map(
              (point) => Padding(
                padding: const EdgeInsets.only(bottom: 10),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text('• '),
                    Expanded(child: Text(point)),
                  ],
                ),
              ),
            )
            .toList(),
      ),
    );
  }

  Widget _buildSourcesCard(ResearchResponse result) {
    return _buildSectionCard(
      title: 'Sources',
      child: Column(
        children: result.sources
            .map(
              (source) => ListTile(
                contentPadding: EdgeInsets.zero,
                leading: const Icon(Icons.link),
                title: Text(source.title),
                subtitle: Text(
                  source.url,
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
                trailing: const Icon(Icons.open_in_new),
                onTap: () => _openUrl(source.url),
              ),
            )
            .toList(),
      ),
    );
  }

  Widget _buildArticleSummariesCard(ResearchResponse result) {
    return _buildSectionCard(
      title: 'Article Summaries',
      child: Column(
        children: result.articles
            .map(
              (article) => ExpansionTile(
                tilePadding: EdgeInsets.zero,
                childrenPadding: const EdgeInsets.only(bottom: 12),
                title: Text(
                  article.title.isEmpty ? 'Untitled Article' : article.title,
                  style: const TextStyle(fontWeight: FontWeight.w600),
                ),
                subtitle: Text(
                  article.url,
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
                children: [
                  Align(
                    alignment: Alignment.centerLeft,
                    child: Text(article.articleSummary),
                  ),
                ],
              ),
            )
            .toList(),
      ),
    );
  }

  Widget _buildResult(ResearchResponse result) {
    return Column(
      children: [
        _buildSummaryCard(result),
        const SizedBox(height: 12),
        _buildKeyPointsCard(result),
        const SizedBox(height: 12),
        _buildSourcesCard(result),
        const SizedBox(height: 12),
        _buildArticleSummariesCard(result),
      ],
    );
  }

  @override
  void dispose() {
    _questionController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('AI Research Assistant'),
      ),
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            _buildInputCard(),
            const SizedBox(height: 16),
            if (_isLoading) _buildLoadingCard(),
            if (_errorMessage != null) _buildErrorCard(_errorMessage!),
            if (!_isLoading && _errorMessage == null && _result == null) _buildEmptyState(),
            if (_result != null) _buildResult(_result!),
          ],
        ),
      ),
    );
  }
}