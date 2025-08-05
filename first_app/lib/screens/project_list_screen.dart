import 'package:flutter/material.dart';
import '../models/project.dart';
import 'project_form.dart';

class ProjectListScreen extends StatefulWidget {
  const ProjectListScreen({Key? key}) : super(key: key);

  @override
  _ProjectListScreenState createState() => _ProjectListScreenState();
}

class _ProjectListScreenState extends State<ProjectListScreen> {
  List<ConstructionProject> projects = [];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Quản lý công trình'),
      ),
      body: ListView.builder(
        itemCount: projects.length,
        itemBuilder: (context, index) {
          final project = projects[index];
          return Card(
            margin: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            child: ExpansionTile(
              title: Text(project.name),
              subtitle: Text(
                'Tổng mức đầu tư: ${project.totalInvestment} VNĐ',
              ),
              children: [
                Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('Kế hoạch vốn: ${project.capitalPlan} VNĐ'),
                      Text('Tổng giải ngân: ${project.totalDisbursement} VNĐ'),
                      SizedBox(height: 8),
                      Text('Thành phần chi phí:',
                          style: Theme.of(context).textTheme.titleMedium),
                      ...project.costComponents.map((component) {
                        return ListTile(
                          title: Text(component.name),
                          subtitle: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              if (component.contractNumber != null)
                                Text('Số HĐ: ${component.contractNumber}'),
                              if (component.contractValue != null)
                                Text('Giá trị HĐ: ${component.contractValue} VNĐ'),
                              if (component.disbursement != null)
                                Text('Giải ngân: ${component.disbursement} VNĐ'),
                            ],
                          ),
                        );
                      }).toList(),
                    ],
                  ),
                ),
              ],
            ),
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () async {
          final result = await Navigator.of(context).push(
            MaterialPageRoute(
              builder: (context) => ProjectForm(),
            ),
          );
          if (result != null && result is ConstructionProject) {
            setState(() {
              projects.add(result);
            });
          }
        },
        child: Icon(Icons.add),
      ),
    );
  }
}
