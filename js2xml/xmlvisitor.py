
from slimit import ast
from lxml.builder import E
import lxml.etree as ET

class XmlVisitor(object):

    def _make_indent(self):
        return ' '

    def visit(self, node):
        method = 'visit_%s' % node.__class__.__name__
        #print method, node,
        #try:
            #print node.value
        #except:
            #print
        return getattr(self, method, self.generic_visit)(node)

    def generic_visit(self, node):
        return 'GEN: %r' % node

    def visit_Program(self, node):
        program = E.program()
        for child in node:
            program.append(self.visit(child))
        return program

    def visit_Block(self, node):
        block = E.block()
        for child in node:
            #print child
            block.append(self.visit(child))
        return block

    def visit_VarStatement(self, node):
        var = E.var()
        for child in node:
            var.append(self.visit(child))
        return var

    def visit_VarDecl(self, node):
        var_decl = E.var_decl()
        var_decl.append(E.identifider(self.visit(node.identifier)))
        if node.initializer is not None:
            var_decl.append(E.initializer(self.visit(node.initializer)))
        return var_decl

    def visit_Identifier(self, node):
        if isinstance(node.value, (int, float)):
            return E.identifier(node.value)
        elif isinstance(node.value, (str, unicode)):
            return E.identifier(node.value)

    def visit_Assign(self, node):
        if node.op == ':':
            template = '%s%s %s'
        else:
            template = '%s %s %s'
        if getattr(node, '_parens', False):
            template = '(%s)' % template
        #print node.__dict__
        assign = E.assign()
        assign.append(E.left(self.visit(node.left)))
        assign.append(E.operator(self.visit_Operator(node.op)))
        assign.append(E.right(self.visit(node.right)))
        return assign

    def visit_GetPropAssign(self, node):
        get = E.get()
        get.append(E.property(self.visit(node.prop_name)))
        body = E.body()
        for el in node.elements:
            body.append(self.visit(el))
        get.append(body)
        return get

    def visit_SetPropAssign(self, node):
        template = 'set %s(%s) {\n%s\n%s}'
        if getattr(node, '_parens', False):
            template = '(%s)' % template
        if len(node.parameters) > 1:
            raise SyntaxError(
                'Setter functions must have one argument: %s' % node)
        params = ','.join(self.visit(param) for param in node.parameters)
        body = '\n'.join(
            (self._make_indent() + self.visit(el))
            for el in node.elements
            )
        tail = self._make_indent()
        return template % (self.visit(node.prop_name), params, body, tail)

    def visit_Number(self, node):
        return E.number(node.value)

    def visit_Comma(self, node):
        comma = E.comma(E.left(self.visit(node.left)),
                        E.right(self.visit(node.right)))
        return comma

    def visit_EmptyStatement(self, node):
        return E.empty(node.value)

    def visit_If(self, node):
        ifel = ET.Element("if")
        if node.predicate is not None:
            ifel.append(E.predicate(self.visit(node.predicate)))
        ifel.append(E.then(self.visit(node.consequent)))
        if node.alternative is not None:
            ifel.append(ET.Element("else", self.visit(node.alternative)))
        return ifel

    def visit_Boolean(self, node):
        return E.boolean(node.value)

    def visit_For(self, node):
        forel = ET.Element("for")
        if node.init is not None:
            forel.append(E.init(self.visit(node.init)))
        if node.init is None:
            forel.append(E.init())
        elif isinstance(node.init, (ast.Assign, ast.Comma, ast.FunctionCall,
                                    ast.UnaryOp, ast.Identifier, ast.BinOp,
                                    ast.Conditional, ast.Regex, ast.NewExpr)):
            pass
        else:
            pass
        if node.cond is not None:
            forel.append(E.condition(self.visit(node.cond)))
        if node.count is not None:
            forel.append(E.post(self.visit(node.count)))
        forel.append(E.statement(self.visit(node.statement)))
        return forel

    def visit_ForIn(self, node):
        if isinstance(node.item, ast.VarDecl):
            template = 'for (var %s in %s) '
        else:
            template = 'for (%s in %s) '
        forel = ET.Element("forin")
        forel.append(E.variable(self.visit(node.item)))
        forel.append(E.object(self.visit(node.iterable)))
        return forel

    def visit_BinOp(self, node):
        binop = E.binaryoperation()
        binop.append(E.left(self.visit(node.left)))
        binop.append(E.operator(self.visit(node.op)))
        binop.append(E.right(self.visit(node.right)))
        return binop

        #if getattr(node, '_parens', False):
            #template = '(%s %s %s)'
        #else:
            #template = '%s %s %s'
        #return template % (
            #self.visit(node.left), node.op, self.visit(node.right))

    def visit_UnaryOp(self, node):
        unary = E.unaryoperation()
        if node.postfix:
            unary.append(self.visit(node.value))
            unary.append(E.operator(self.visit(node.op)))
        elif node.op in ('delete', 'void', 'typeof'):
            #s = '%s %s' % (node.op, s)
            unary.append(E.operation(node.op))
            unary.append(self.visit(node.value))
        else:
            unary.append(E.operation(node.op))
            unary.append(self.visit(node.value))
        return unary

    def visit_ExprStatement(self, node):
        return self.visit(node.expr)

    def visit_DoWhile(self, node):
        dowhile = E.dowhile()
        dowhile.append(E.statement(self.visit(node.statement)))
        dowhile.append(ET.Element("while", self.visit(node.predicate)))
        return dowhile

    def visit_While(self, node):
        whileel = ET.Element("while")
        whileel.append(E.predicate(self.visit(node.predicate)))
        whileel.append(E.statement(self.visit(node.statement)))
        return whileel

    def visit_Null(self, node):
        return E.null()

    def visit_Operator(self, node):
        try:
            return node.value
        except:
            return node

    def visit_str(self, node):
        return node

    def visit_String(self, node):
        return E.string(node.value.strip('"\''))

    def visit_Continue(self, node):
        continueel = ET.Element("continue")
        if node.identifier is not None:
            continueel.append(self.visit_Identifier(node.identifier))
        return continueel

    def visit_Break(self, node):
        breakel = ET.Element("break")
        if node.identifier is not None:
            breakel.append(self.visit_Identifier(node.identifier))
        return breakel

    def visit_Return(self, node):
        ret = ET.Element("return")
        if node.expr is not None:
            ret.append(self.visit(node.expr))
        return ret

    def visit_With(self, node):
        withel = ET.Element("with")
        withel.append(self.visit(node.expr))
        withel.append(E.statement(self.visit(node.statement)))
        return withel

    def visit_Label(self, node):
        label = E.label()
        label.append(E.identifier(self.visit(node.identifier)))
        label.append(E.statement(self.visit(node.statement)))
        return label

    def visit_Switch(self, node):
        switch = E.switch(E.expression(self.visit(node.expr)))
        for case in node.cases:
            switch.append(self.visit_Case(case))
        if node.default is not None:
            switch.append(self.visit_Default(node.default))
        return switch

    def visit_Case(self, node):
        case = E.case()
        case.append(E.expression(self.visit(node.expr)))
        for element in node.elements:
            case.append(self.visit(element))
        return case

    def visit_Default(self, node):
        default = E.default()
        for element in node.elements:
            default.append(self.visit(element))
        return default

    def visit_Throw(self, node):
        return E.throw(self.visit(node.expr))

    def visit_Debugger(self, node):
        return E.debugger(node.value)

    def visit_Try(self, node):
        tryel = ET.Element("try")
        tryel.append(E.statements(self.visit(node.statements)))
        if node.catch is not None:
            tryel.append(self.visit(node.catch))
        if node.fin is not None:
            tryel.append(self.visit(node.fin))
        return tryel

    def visit_Catch(self, node):
        return E.catch(E.expression(self.visit(node.identifier)),
                       E.body(self.visit(node.elements)))

    def visit_Finally(self, node):
        return ET.Element("finally", self.visit(node.elements))

    def visit_FuncDecl(self, node):
        funcdecl = E.funcdecl()
        if node.identifier is not None:
            funcdecl.append(self.visit(node.identifier))
        else:
            funcdecl.append(E.identifier())
        parameters = E.parameters()
        for param in node.parameters:
            parameters.append(self.visit(param))
        funcdecl.append(parameters)
        funcbody = E.body()
        for element in node.elements:
            funcbody.append(self.visit(element))
        funcdecl.append(funcbody)
        return funcdecl

    def visit_FuncExpr(self, node):
        funcexpr = E.funcexpr()
        if node.identifier is not None:
            funcexpr.append(self.visit(node.identifier))
        else:
            funcexpr.append(E.identifier())
        parameters = E.parameters()
        for param in node.parameters:
            parameters.append(self.visit(param))
        funcexpr.append(parameters)
        body = E.body()
        for element in node.elements:
            body.append(self.visit(element))
        funcexpr.append(body)
        return funcexpr

    def visit_Conditional(self, node):
        conditional = E.conditional()
        conditional.append(E.condition(self.visit(node.predicate)))
        conditional.append(E.value1(self.visit(node.consequent)))
        conditional.append(E.value2(self.visit(node.alternative)))
        return conditional

    def visit_Regex(self, node):
        return E.regex(node.value)

    def visit_NewExpr(self, node):
        newel = E.new()
        newel.append(self.visit(node.identifier))
        arguments = E.arguments()
        for arg in node.args:
            arguments.append(self.visit(arg))
        newel.append(arguments)
        return newel

    def visit_DotAccessor(self, node):
        dot = E.dotaccessor()
        dot.append(E.object(self.visit(node.node)))
        dot.append(E.property(self.visit(node.identifier)))
        return dot

    def visit_BracketAccessor(self, node):
        bracket = E.bracketaccessor(E.object(self.visit(node.node)),
                                    E.property(self.visit(node.expr)))
        return bracket

    def visit_FunctionCall(self, node):
        funccall = E.functioncall()
        funccall.append(E.identifier(self.visit(node.identifier)))
        arguments = E.arguments()
        for arg in node.args:
            arguments.append(self.visit(arg))
        funccall.append(arguments)
        return funccall

    def visit_Object(self, node):
        obj = ET.Element("object")
        for prop in node.properties:
            obj.append(self.visit(prop))
        return obj

    def visit_Array(self, node):
        array = E.array()
        length = len(node.items) - 1
        for index, item in enumerate(node.items):
            if isinstance(item, ast.Elision):
                pass
            else:
                array.append(self.visit(item))
        return array

    def visit_This(self, node):
        return E.identifier('this')

