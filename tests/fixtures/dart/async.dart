Future<String> fetchData() async {
  await Future.delayed(Duration(seconds: 1));
  return "data";
}

void main() async {
  final data = await fetchData();
  print(data);
}