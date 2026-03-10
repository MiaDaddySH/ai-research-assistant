import 'package:flutter/material.dart';

class ResearchScreen extends StatelessWidget {
  const ResearchScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('AI Research Assistant'),
      ),
      body: const Center(
        child: Text('Step 1: Frontend initialized'),
      ),
    );
  }
}