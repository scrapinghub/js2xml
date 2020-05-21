import ast as pyast
import re

from calmjs.parse import asttypes as ast
from lxml.builder import E
import lxml.etree as ET
import six


invalid_unicode_re = re.compile(u"""[\u0001-\u0008\u000b\u000e-\u001f\u007f]""", re.U)
surrogate_unicode_re = re.compile(u'[\\ud800-\\udbff][\\udc00-\\udfff]', re.U)


def unescape_string(input_string):
    input_string = invalid_unicode_re.sub(u"\ufffd", input_string)
    return input_string.replace(r'\/', '/')


class XmlVisitor(object):

    def visit(self, node):
        method = 'visit_%s' % node.__class__.__name__
        return getattr(self, method, self.generic_visit)(node)

    def generic_visit(self, node):
        return 'GEN: %r' % node

    def visit_ES5Program(self, node):
        program = E.program()
        for child in node:
            program.extend(self.visit(child))
        return program

    def visit_Block(self, node):
        block = E.block()
        for child in node:
            block.extend(self.visit(child))
        return [block]

    def visit_VarStatement(self, node):
        return [el for child in node for el in self.visit(child)]

    def visit_VarDecl(self, node):
        identifier = self.visit(node.identifier)[0]
        varel = E.var(name=identifier.get("name"))
        if node.initializer is not None:
            varel.extend(self.visit(node.initializer))
        return [varel]

    def visit_VarDeclNoIn(self, node):
        return self.visit_VarDecl(node)

    def visit_Identifier(self, node):
        if isinstance(node.value, (int, float)):
            return [E.identifier(node.value)]
        elif isinstance(node.value, six.string_types):
            if node.value == "undefined":
                return [E.undefined()]
            idel = E.identifier()
            idel.attrib["name"] = node.value
            return [idel]

    def visit_PropIdentifier(self, node):
        return self.visit_Identifier(node)

    def visit_Assign(self, node):
        if node.op == ':':
            propname = self.visit(node.left)[0]
            if isinstance(node.left, ast.String):
                propel = E.property(name=propname.text)
            elif isinstance(node.left, ast.Identifier):
                propel = E.property(name=propname.get("name"))
            elif isinstance(node.left, ast.Number):
                propel = E.property(name=propname.get("value"))
            else:
                print(type(node.left), type(propname))
                raise RuntimeError

            propel.extend(self.visit(node.right))
            return [propel]
        else:
            assign = E.assign(operator=node.op)
            left = E.left()
            left.extend(self.visit(node.left))
            right = E.right()
            right.extend(self.visit(node.right))
            assign.append(left)
            assign.append(right)
            return [assign]

    def visit_GetPropAssign(self, node):
        propel = E.property()
        propel.extend(self.visit(node.prop_name))
        getel = E.get()
        getel.append(propel)
        body = E.body()
        for el in node.elements:
            body.extend(self.visit(el))
        getel.append(body)
        return [getel]

    def visit_SetPropAssign(self, node):
        propel = E.property()
        propel.extend(self.visit(node.prop_name))
        setel = ET.Element("set")
        params = E.params()
        params.extend(self.visit(node.parameter))
        body = E.body()
        for el in node.elements:
            body.extend(self.visit(el))
        setel.append(body)
        return [setel]

    def visit_Number(self, node):
        return [E.number(value=node.value)]

    def visit_Comma(self, node):
        comma = E.comma(E.left(self.visit(node.left)[0]),
                        E.right(self.visit(node.right)[0]))
        return [comma]

    def visit_EmptyStatement(self, node):
        return [E.empty(node.value)]

    def visit_If(self, node):
        ifel = ET.Element("if")
        if node.predicate is not None:
            predicate = E.predicate()
            predicate.extend(self.visit(node.predicate))
            ifel.append(predicate)

        then = E.then()
        then.extend(self.visit(node.consequent))
        ifel.append(then)

        if node.alternative is not None:
            elseel = ET.Element("else")
            elseel.extend(self.visit(node.alternative))
            ifel.append(elseel)

        return [ifel]

    def visit_Boolean(self, node):
        return [E.boolean(node.value)]

    def visit_For(self, node):
        forel = ET.Element("for")
        if node.init is not None:
            initel = E.init()
            initel.extend(self.visit(node.init))
            forel.append(initel)
        if node.init is None:
            forel.extend(E.init())
        if node.cond is not None:
            condition = E.condition()
            condition.extend(self.visit(node.cond))
            forel.append(condition)

        if node.count is not None:
            post = E.post()
            post.extend(self.visit(node.count))
            forel.append(post)

        statement = E.statement()
        statement.extend(self.visit(node.statement))
        forel.append(statement)
        return [forel]

    def visit_ForIn(self, node):
        variable = E.variable()
        variable.extend(self.visit(node.item))

        objel = ET.Element("object")
        objel.extend(self.visit(node.iterable))

        forel = ET.Element("forin")
        forel.append(variable)
        forel.append(objel)

        statement = E.statement()
        statement.extend(self.visit(node.statement))
        forel.append(statement)

        return [forel]

    def visit_BinOp(self, node):
        binop = E.binaryoperation(operation=node.op)
        leftpart = E.left()
        leftpart.extend(self.visit(node.left))
        binop.append(leftpart)
        rightpart = E.right(*self.visit(node.right))
        binop.append(rightpart)
        return [binop]

    def visit_PostfixExpr(self, node):
        postfix = E.postfix(operation=node.op)
        postfix.extend(self.visit(node.value))
        return [postfix]

    def visit_UnaryExpr(self, node):
        if node.op in ('delete', 'void', 'typeof'):
            unary = E.unaryoperation(operation=node.op)
            unary.extend(self.visit(node.value))
        else:
            # convert things like "+3.14" and "-22"
            if node.op in ("-", "+") and isinstance(node.value, ast.Number):
                node.value.value = "%s%s" % (node.op, node.value.value)
                return self.visit(node.value)
            else:
                unary = E.unaryoperation(operation=node.op)
                unary.extend(self.visit(node.value))
        return [unary]

    def visit_ExprStatement(self, node):
        return self.visit(node.expr)

    def visit_DoWhile(self, node):
        dowhile = E.dowhile()
        statement = E.statement()
        statement.extend(self.visit(node.statement))
        dowhile.append(statement)
        whileel = ET.Element("while")
        whileel.extend(self.visit(node.predicate))
        dowhile.append(whileel)
        return dowhile

    def visit_While(self, node):
        whileel = ET.Element("while")
        predicate = E.predicate()
        predicate.extend(self.visit(node.predicate))
        whileel.append(predicate)
        statement = E.statement()
        statement.extend(self.visit(node.statement))
        whileel.append(statement)
        return [whileel]

    def visit_Null(self, node):
        return [E.null()]

    def visit_Operator(self, node):
        try:
            return node.value
        except:
            return node

    def visit_str(self, node):
        return node

    def visit_String(self, node):
        str_value = pyast.literal_eval("u"+node.value)
        if surrogate_unicode_re.search(str_value):
            in_utf16 = str_value.encode('utf16', 'surrogatepass')
            str_value = in_utf16.decode('utf16')
        return [E.string(unescape_string(str_value))]

    def visit_Continue(self, node):
        continueel = ET.Element("continue")
        if node.identifier is not None:
            continueel.extend(self.visit_Identifier(node.identifier))
        return [continueel]

    def visit_Break(self, node):
        breakel = ET.Element("break")
        if node.identifier is not None:
            breakel.extend(self.visit_Identifier(node.identifier))
        return [breakel]

    def visit_Return(self, node):
        ret = ET.Element("return")
        if node.expr is not None:
            ret.extend(self.visit(node.expr))
        return [ret]

    def visit_With(self, node):
        withel = ET.Element("with")
        withel.extend(self.visit(node.expr))
        statement = E.statement()
        statement.extend(self.visit(node.statement))
        withel.append(statement)
        return [withel]

    def visit_Label(self, node):
        identifier = self.visit(node.identifier)[0]
        label = E.label(name=identifier.get("name"))
        statement = E.statement()
        statement.extend(self.visit(node.statement))
        label.append(statement)
        return [label]

    def visit_Switch(self, node):
        expression = E.expression()
        expression.extend(self.visit(node.expr))
        switch = E.switch()
        switch.append(expression)
        for child in node.case_block.children():
            switch.extend(self.visit(child))
        return [switch]

    def visit_Case(self, node):
        expression = E.expression()
        expression.extend(self.visit(node.expr))
        case = E.case()
        case.append(expression)
        for element in node.elements:
            case.extend(self.visit(element))
        return [case]

    def visit_Default(self, node):
        default = E.default()
        for element in node.elements:
            default.extend(self.visit(element))
        return [default]

    def visit_Throw(self, node):
        throwel = E.throw()
        throwel.extend(self.visit(node.expr))
        return [throwel]

    def visit_Debugger(self, node):
        return [E.debugger(node.value)]

    def visit_Try(self, node):
        tryel = ET.Element("try")
        statements = E.statements()
        statements.extend(self.visit(node.statements))
        tryel.append(statements)
        if node.catch is not None:
            tryel.extend(self.visit(node.catch))
        if node.fin is not None:
            tryel.extend(self.visit(node.fin))
        return [tryel]

    def visit_Catch(self, node):
        expression = E.expression()
        expression.extend(self.visit(node.identifier))
        body = E.body()
        body.extend(self.visit(node.elements))
        return [E.catch(expression, body)]

    def visit_Finally(self, node):
        finallyel = ET.Element("finally")
        finallyel.extend(self.visit(node.elements))
        return [finallyel]

    def visit_FuncDecl(self, node):
        funcdecl = E.funcdecl()

        if node.identifier is not None:
            identifier = self.visit(node.identifier)[0]
            funcdecl.attrib["name"] = identifier.get("name")

        parameters = E.parameters()
        for param in node.parameters:
            parameters.extend(self.visit(param))
        funcdecl.append(parameters)
        funcbody = E.body()
        for element in node.elements:
            funcbody.extend(self.visit(element))
        funcdecl.append(funcbody)
        return [funcdecl]

    def visit_FuncExpr(self, node):
        funcexpr = E.funcexpr()
        if node.identifier is not None:
            funcexpr.extend(self.visit(node.identifier))
        else:
            funcexpr.append(E.identifier())
        parameters = E.parameters()
        for param in node.parameters:
            parameters.extend(self.visit(param))
        funcexpr.append(parameters)
        body = E.body()
        for element in node.elements:
            body.extend(self.visit(element))
        funcexpr.append(body)
        return [funcexpr]

    def visit_Conditional(self, node):
        conditional = E.conditional()

        condition = E.condition()
        condition.extend(self.visit(node.predicate))

        value1 = E.value1()
        value1.extend(self.visit(node.consequent))
        value2 = E.value2()
        value2.extend(self.visit(node.alternative))

        conditional.append(condition)
        conditional.append(value1)
        conditional.append(value2)

        return [conditional]

    def visit_Regex(self, node):
        return [E.regex(node.value)]

    def visit_NewExpr(self, node):
        newel = E.new()
        newel.extend(self.visit(node.identifier))
        arguments = E.arguments()
        for arg in node.args:
            arguments.extend(self.visit(arg))
        newel.append(arguments)
        return [newel]

    def visit_DotAccessor(self, node):
        dot = E.dotaccessor()
        objel = E.object()
        objel.extend(self.visit(node.node))
        propel = E.property()
        propel.extend(self.visit(node.identifier))
        dot.append(objel)
        dot.append(propel)
        return [dot]

    def visit_BracketAccessor(self, node):
        objel = E.object()
        objel.extend(self.visit(node.node))
        propel = E.property()
        propel.extend(self.visit(node.expr))
        bracket = E.bracketaccessor(objel, propel)
        return [bracket]

    def visit_FunctionCall(self, node):
        function = E.function()
        function.extend(self.visit(node.identifier))
        funccall = E.functioncall(function)
        arguments = E.arguments()
        for arg in node.args:
            arguments.extend(self.visit(arg))
        funccall.append(arguments)
        return [funccall]

    def visit_GroupingOp(self, node):
        op = E.groupingoperator()
        op.extend(self.visit(node.expr))
        return [op]

    def visit_Object(self, node):
        obj = ET.Element("object")
        for prop in node.properties:
            obj.extend(self.visit(prop))
        return [obj]

    def visit_Array(self, node):
        array = E.array()
        for index, item in enumerate(node.items):
            if isinstance(item, ast.Elision):
                for _ in range(item.value):
                    array.append(E.undefined())
            else:
                array.extend(self.visit(item))
        return [array]

    def visit_This(self, node):
        return [E.identifier('this')]

