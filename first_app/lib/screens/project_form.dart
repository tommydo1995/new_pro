import 'package:flutter/material.dart';
import '../constants/cost_components.dart';
import '../models/project.dart';

class ProjectForm extends StatefulWidget {
  final ConstructionProject? project;

  const ProjectForm({Key? key, this.project}) : super(key: key);

  @override
  _ProjectFormState createState() => _ProjectFormState();
}

class _ProjectFormState extends State<ProjectForm> {
  final _formKey = GlobalKey<FormState>();
  late TextEditingController _nameController;
  late TextEditingController _totalInvestmentController;
  late TextEditingController _capitalPlanController;
  Map<String, bool> selectedComponents = {};
  Map<String, TextEditingController> contractNumberControllers = {};
  Map<String, TextEditingController> contractValueControllers = {};
  Map<String, TextEditingController> disbursementControllers = {};

  @override
  void initState() {
    super.initState();
    _nameController = TextEditingController(text: widget.project?.name ?? '');
    _totalInvestmentController = TextEditingController(
        text: widget.project?.totalInvestment.toString() ?? '');
    _capitalPlanController = TextEditingController(
        text: widget.project?.capitalPlan.toString() ?? '');

    // Initialize cost components
    for (var type in CostComponentTypes.types) {
      selectedComponents[type] = false;
      contractNumberControllers[type] = TextEditingController();
      contractValueControllers[type] = TextEditingController();
      disbursementControllers[type] = TextEditingController();
    }

    // If editing existing project, populate the form
    if (widget.project != null) {
      for (var component in widget.project!.costComponents) {
        selectedComponents[component.name] = true;
        contractNumberControllers[component.name]?.text = component.contractNumber ?? '';
        contractValueControllers[component.name]?.text = component.contractValue?.toString() ?? '';
        disbursementControllers[component.name]?.text = component.disbursement?.toString() ?? '';
      }
    }
  }

  @override
  void dispose() {
    _nameController.dispose();
    _totalInvestmentController.dispose();
    _capitalPlanController.dispose();
    contractNumberControllers.values.forEach((controller) => controller.dispose());
    contractValueControllers.values.forEach((controller) => controller.dispose());
    disbursementControllers.values.forEach((controller) => controller.dispose());
    super.dispose();
  }

  void _submitForm() {
    if (_formKey.currentState!.validate()) {
      List<CostComponent> components = [];
      for (var type in CostComponentTypes.types) {
        if (selectedComponents[type] == true) {
          components.add(CostComponent(
            name: type,
            contractNumber: contractNumberControllers[type]?.text,
            contractValue: double.tryParse(contractValueControllers[type]?.text ?? ''),
            disbursement: double.tryParse(disbursementControllers[type]?.text ?? ''),
          ));
        }
      }

      final project = ConstructionProject(
        name: _nameController.text,
        totalInvestment: double.parse(_totalInvestmentController.text),
        costComponents: components,
        capitalPlan: double.parse(_capitalPlanController.text),
        totalDisbursement: components
            .map((e) => e.disbursement ?? 0.0)
            .reduce((a, b) => a + b),
      );

      Navigator.of(context).pop(project);
    }
  }

  Widget _buildCostComponentTile(String type) {
    return ExpansionTile(
      title: Row(
        children: [
          Checkbox(
            value: selectedComponents[type],
            onChanged: (bool? value) {
              setState(() {
                selectedComponents[type] = value ?? false;
              });
            },
          ),
          Text(type),
        ],
      ),
      children: [
        if (selectedComponents[type] == true) ...[
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Column(
              children: [
                TextFormField(
                  controller: contractNumberControllers[type],
                  decoration: InputDecoration(
                    labelText: 'Số hợp đồng',
                    border: OutlineInputBorder(),
                  ),
                ),
                SizedBox(height: 8),
                TextFormField(
                  controller: contractValueControllers[type],
                  decoration: InputDecoration(
                    labelText: 'Giá trị hợp đồng',
                    border: OutlineInputBorder(),
                  ),
                  keyboardType: TextInputType.number,
                ),
                SizedBox(height: 8),
                TextFormField(
                  controller: disbursementControllers[type],
                  decoration: InputDecoration(
                    labelText: 'Giải ngân',
                    border: OutlineInputBorder(),
                  ),
                  keyboardType: TextInputType.number,
                ),
              ],
            ),
          ),
        ],
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.project == null ? 'Thêm công trình mới' : 'Sửa công trình'),
      ),
      body: Form(
        key: _formKey,
        child: ListView(
          padding: EdgeInsets.all(16.0),
          children: [
            TextFormField(
              controller: _nameController,
              decoration: InputDecoration(
                labelText: 'Tên công trình',
                border: OutlineInputBorder(),
              ),
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return 'Vui lòng nhập tên công trình';
                }
                return null;
              },
            ),
            SizedBox(height: 16),
            TextFormField(
              controller: _totalInvestmentController,
              decoration: InputDecoration(
                labelText: 'Tổng mức đầu tư',
                border: OutlineInputBorder(),
              ),
              keyboardType: TextInputType.number,
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return 'Vui lòng nhập tổng mức đầu tư';
                }
                if (double.tryParse(value) == null) {
                  return 'Vui lòng nhập số hợp lệ';
                }
                return null;
              },
            ),
            SizedBox(height: 16),
            TextFormField(
              controller: _capitalPlanController,
              decoration: InputDecoration(
                labelText: 'Kế hoạch vốn',
                border: OutlineInputBorder(),
              ),
              keyboardType: TextInputType.number,
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return 'Vui lòng nhập kế hoạch vốn';
                }
                if (double.tryParse(value) == null) {
                  return 'Vui lòng nhập số hợp lệ';
                }
                return null;
              },
            ),
            SizedBox(height: 16),
            Card(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Padding(
                    padding: const EdgeInsets.all(8.0),
                    child: Text(
                      'Thành phần chi phí',
                      style: Theme.of(context).textTheme.titleLarge,
                    ),
                  ),
                  ...CostComponentTypes.types
                      .map((type) => _buildCostComponentTile(type))
                      .toList(),
                ],
              ),
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _submitForm,
        child: Icon(Icons.save),
      ),
    );
  }
}
