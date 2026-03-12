import 'package:flutter_test/flutter_test.dart';

import 'package:frontend/main.dart';

void main() {
  testWidgets('Research screen renders expected initial UI', (WidgetTester tester) async {
    await tester.pumpWidget(const MyApp());

    expect(find.text('AI Research Assistant'), findsOneWidget);
    expect(find.text('Research Question'), findsOneWidget);
    expect(find.text('Start Research'), findsOneWidget);
    expect(
      find.text('What are the latest developments in AI coding assistants?'),
      findsWidgets,
    );
  });
}
