import subprocess
import os
import tempfile
import shutil
import platform
from django.conf import settings
import signal


class CodeExecutor:
    """Handles secure code execution for multiple programming languages"""
    
    def __init__(self):
        self.timeout = getattr(settings, 'CODE_EXECUTION_TIMEOUT', 10)
        self.execution_dir = getattr(settings, 'EXECUTION_DIR', None)
        if not self.execution_dir:
            self.execution_dir = tempfile.mkdtemp()
    
    def execute(self, language, code, input_data=''):
        """Execute code based on language"""
        handlers = {
            'c': self._execute_c,
            'cpp': self._execute_cpp,
            'java': self._execute_java,
            'python': self._execute_python,
        }
        
        handler = handlers.get(language.lower())
        if not handler:
            return {'success': False, 'error': f'Unsupported language: {language}'}
        
        try:
            return handler(code, input_data)
        except Exception as e:
            return {'success': False, 'error': f'Execution error: {str(e)}'}
    
    def _execute_c(self, code, input_data):
        """Execute C code"""
        temp_dir = tempfile.mkdtemp(dir=self.execution_dir)
        try:
            source_file = os.path.join(temp_dir, 'program.c')
            # Add .exe extension on Windows
            executable_name = 'program.exe' if platform.system() == 'Windows' else 'program'
            executable = os.path.join(temp_dir, executable_name)
            
            with open(source_file, 'w', encoding='utf-8') as f:
                f.write(code)
            
            # Compile
            compile_cmd = ['gcc', source_file, '-o', executable, '-lm', '-std=c11']
            compile_result = subprocess.run(
                compile_cmd,
                capture_output=True,
                text=True,
                timeout=5,
                cwd=temp_dir
            )
            
            if compile_result.returncode != 0:
                return {
                    'success': False,
                    'error': compile_result.stderr
                }
            
            # Execute
            run_result = subprocess.run(
                [executable],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=temp_dir
            )
            
            return {
                'success': run_result.returncode == 0,
                'output': run_result.stdout,
                'error': run_result.stderr if run_result.returncode != 0 else ''
            }
        
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    def _execute_cpp(self, code, input_data):
        """Execute C++ code"""
        temp_dir = tempfile.mkdtemp(dir=self.execution_dir)
        try:
            source_file = os.path.join(temp_dir, 'program.cpp')
            # Add .exe extension on Windows
            executable_name = 'program.exe' if platform.system() == 'Windows' else 'program'
            executable = os.path.join(temp_dir, executable_name)
            
            with open(source_file, 'w', encoding='utf-8') as f:
                f.write(code)
            
            # Compile
            compile_cmd = ['g++', source_file, '-o', executable, '-std=c++17']
            compile_result = subprocess.run(
                compile_cmd,
                capture_output=True,
                text=True,
                timeout=5,
                cwd=temp_dir
            )
            
            if compile_result.returncode != 0:
                return {
                    'success': False,
                    'error': compile_result.stderr
                }
            
            # Execute
            run_result = subprocess.run(
                [executable],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=temp_dir
            )
            
            return {
                'success': run_result.returncode == 0,
                'output': run_result.stdout,
                'error': run_result.stderr if run_result.returncode != 0 else ''
            }
        
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    def _execute_java(self, code, input_data):
        """Execute Java code"""
        temp_dir = tempfile.mkdtemp(dir=self.execution_dir)
        try:
            # Extract class name from code (simple heuristic)
            class_name = 'Main'
            if 'class' in code:
                for line in code.split('\n'):
                    if 'class' in line and '{' in line:
                        parts = line.split()
                        if 'class' in parts:
                            idx = parts.index('class')
                            if idx + 1 < len(parts):
                                class_name = parts[idx + 1].split('{')[0].strip()
                                break
            
            source_file = os.path.join(temp_dir, f'{class_name}.java')
            
            with open(source_file, 'w', encoding='utf-8') as f:
                f.write(code)
            
            # Compile
            compile_cmd = ['javac', source_file]
            compile_result = subprocess.run(
                compile_cmd,
                capture_output=True,
                text=True,
                timeout=5,
                cwd=temp_dir
            )
            
            if compile_result.returncode != 0:
                return {
                    'success': False,
                    'error': compile_result.stderr
                }
            
            # Execute
            run_result = subprocess.run(
                ['java', '-cp', temp_dir, class_name],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=temp_dir
            )
            
            return {
                'success': run_result.returncode == 0,
                'output': run_result.stdout,
                'error': run_result.stderr if run_result.returncode != 0 else ''
            }
        
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    def _execute_python(self, code, input_data):
        """Execute Python code"""
        temp_dir = tempfile.mkdtemp(dir=self.execution_dir)
        try:
            script_file = os.path.join(temp_dir, 'program.py')
            
            with open(script_file, 'w', encoding='utf-8') as f:
                f.write(code)
            
            # Use python3 on Unix, python on Windows
            python_cmd = 'python3' if platform.system() != 'Windows' else 'python'
            
            # Execute
            run_result = subprocess.run(
                [python_cmd, script_file],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=temp_dir
            )
            
            return {
                'success': run_result.returncode == 0,
                'output': run_result.stdout,
                'error': run_result.stderr if run_result.returncode != 0 else ''
            }
        
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

