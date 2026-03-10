import 'package:flutter/material.dart';
import 'screens/research_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AI Research Assistant',
      theme: ThemeData(
        useMaterial3: true,
      ),
      home: const ResearchScreen(),
    );
  }
}