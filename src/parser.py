"""
Squawk Parser - Builds Abstract Syntax Tree from tokens
"""

from typing import List, Optional
from lexer import Token, TokenType
from ast_nodes import *


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def error(self, msg: str):
        if self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            raise SyntaxError(f"Parser error at line {token.line}, column {token.column}: {msg}")
        raise SyntaxError(f"Parser error at end of file: {msg}")
    
    def peek(self, offset: int = 0) -> Optional[Token]:
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None
    
    def advance(self) -> Token:
        token = self.tokens[self.pos]
        self.pos += 1
        return token
    
    def expect(self, token_type: TokenType) -> Token:
        token = self.peek()
        if not token or token.type != token_type:
            self.error(f"Expected {token_type}, got {token.type if token else 'EOF'}")
        return self.advance()
    
    def skip_newlines(self):
        while self.peek() and self.peek().type == TokenType.NEWLINE:
            self.advance()
    
    def parse_type(self) -> Type:
        self.skip_newlines()
        token = self.peek()
        if token.type == TokenType.INT_TYPE:
            self.advance()
            return Type.INT
        elif token.type == TokenType.BOOL_TYPE:
            self.advance()
            return Type.BOOL
        else:
            self.error(f"Expected type, got {token.type}")
    
    def parse_primary(self) -> ASTNode:
        self.skip_newlines()
        token = self.peek()
        
        # Integer literal
        if token.type == TokenType.INTEGER:
            self.advance()
            return IntLiteral(token.value)
        
        # Boolean literals
        if token.type == TokenType.TRUE:
            self.advance()
            return BoolLiteral(True)
        
        if token.type == TokenType.FALSE:
            self.advance()
            return BoolLiteral(False)
        
        # Parenthesized expression
        if token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        
        # If expression
        if token.type == TokenType.IF:
            return self.parse_if_expr()
        
        # Let expression
        if token.type == TokenType.LET:
            return self.parse_let_expr()
        
        # Variable or function call
        if token.type == TokenType.IDENTIFIER:
            name = token.value
            self.advance()
            
            # Check if it's a function call
            if self.peek() and self.peek().type == TokenType.LPAREN:
                self.advance()
                args = []
                
                if self.peek().type != TokenType.RPAREN:
                    args.append(self.parse_expression())
                    while self.peek() and self.peek().type == TokenType.COMMA:
                        self.advance()
                        args.append(self.parse_expression())
                
                self.expect(TokenType.RPAREN)
                return CallExpr(name, args)
            else:
                return Variable(name)
        
        self.error(f"Unexpected token: {token.type}")
    
    def parse_if_expr(self) -> IfExpr:
        self.expect(TokenType.IF)
        condition = self.parse_expression()
        self.skip_newlines()
        self.expect(TokenType.THEN)
        then_expr = self.parse_expression()
        self.skip_newlines()
        self.expect(TokenType.ELSE)
        else_expr = self.parse_expression()
        return IfExpr(condition, then_expr, else_expr)
    
    def parse_let_expr(self) -> LetExpr:
        self.expect(TokenType.LET)
        name_token = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.EQUALS)
        value = self.parse_expression()
        self.skip_newlines()
        self.expect(TokenType.IN)
        body = self.parse_expression()
        return LetExpr(name_token.value, value, body)
    
    def parse_multiplicative(self) -> ASTNode:
        left = self.parse_primary()
        
        while self.peek() and self.peek().type in [TokenType.MULTIPLY, TokenType.DIVIDE]:
            op_token = self.advance()
            right = self.parse_primary()
            
            if op_token.type == TokenType.MULTIPLY:
                left = BinaryExpr(BinaryOp.MULTIPLY, left, right)
            else:
                left = BinaryExpr(BinaryOp.DIVIDE, left, right)
        
        return left
    
    def parse_additive(self) -> ASTNode:
        left = self.parse_multiplicative()
        
        while self.peek() and self.peek().type in [TokenType.PLUS, TokenType.MINUS]:
            op_token = self.advance()
            right = self.parse_multiplicative()
            
            if op_token.type == TokenType.PLUS:
                left = BinaryExpr(BinaryOp.ADD, left, right)
            else:
                left = BinaryExpr(BinaryOp.SUBTRACT, left, right)
        
        return left
    
    def parse_comparison(self) -> ASTNode:
        left = self.parse_additive()
        
        comparison_ops = {
            TokenType.DOUBLE_EQUALS: BinaryOp.EQUAL,
            TokenType.NOT_EQUALS: BinaryOp.NOT_EQUAL,
            TokenType.LESS_THAN: BinaryOp.LESS_THAN,
            TokenType.GREATER_THAN: BinaryOp.GREATER_THAN,
            TokenType.LESS_EQUAL: BinaryOp.LESS_EQUAL,
            TokenType.GREATER_EQUAL: BinaryOp.GREATER_EQUAL,
        }
        
        while self.peek() and self.peek().type in comparison_ops:
            op_token = self.advance()
            right = self.parse_additive()
            left = BinaryExpr(comparison_ops[op_token.type], left, right)
        
        return left
    
    def parse_expression(self) -> ASTNode:
        return self.parse_comparison()
    
    def parse_parameter(self) -> Parameter:
        self.skip_newlines()
        name_token = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.COLON)
        param_type = self.parse_type()
        return Parameter(name_token.value, param_type)
    
    def parse_function(self) -> FunctionDef:
        self.skip_newlines()
        self.expect(TokenType.FN)
        
        name_token = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.LPAREN)
        
        # Parse parameters
        parameters = []
        if self.peek().type != TokenType.RPAREN:
            parameters.append(self.parse_parameter())
            while self.peek() and self.peek().type == TokenType.COMMA:
                self.advance()
                parameters.append(self.parse_parameter())
        
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.ARROW)
        
        return_type = self.parse_type()
        self.expect(TokenType.EQUALS)
        
        body = self.parse_expression()
        
        return FunctionDef(name_token.value, parameters, return_type, body)
    
    def parse_program(self) -> Program:
        functions = []
        
        self.skip_newlines()
        while self.peek() and self.peek().type != TokenType.EOF:
            functions.append(self.parse_function())
            self.skip_newlines()
        
        return Program(functions)
